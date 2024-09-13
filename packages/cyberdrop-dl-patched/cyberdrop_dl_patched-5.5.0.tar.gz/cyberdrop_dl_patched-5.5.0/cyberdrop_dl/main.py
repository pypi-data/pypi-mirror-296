import asyncio
import contextlib
import logging
import os
import sys
import traceback


from cyberdrop_dl.managers.manager import Manager
from cyberdrop_dl.scraper.scraper import ScrapeMapper
from cyberdrop_dl.ui.ui import program_ui
from cyberdrop_dl.utils.sorting import Sorter
from cyberdrop_dl.utils.utilities import check_latest_pypi, log_with_color, check_partials_and_empty_folders, log
from cyberdrop_dl.managers.console_manager import print_


def startup() -> Manager:
    """
    Starts the program and returns the manager
    This will also run the UI for the program
    After this function returns, the manager will be ready to use and scraping / downloading can begin
    """

    try:
        manager = Manager()
        manager.startup()

        if not manager.args_manager.immediate_download:
            program_ui(manager)

        return manager

    except KeyboardInterrupt:
        print_("\nExiting...")
        exit(0)


async def runtime(manager: Manager) -> None:
    """Main runtime loop for the program, this will run until all scraping and downloading is complete"""
    scrape_mapper = ScrapeMapper(manager)

    # NEW CODE
    async with asyncio.TaskGroup() as task_group:
        manager.task_group = task_group
        await scrape_mapper.start()

    
async def post_runtime(manager: Manager) -> None:
    """Actions to complete after main runtime, and before ui shutdown"""
    #checking and removing dupes
    await manager.hash_manager.hash_client.cleanup_dupes()
    

async def director(manager: Manager) -> None:
    """Runs the program and handles the UI"""
    configs = manager.config_manager.get_configs()
    configs_ran = []
    manager.path_manager.startup()
    manager.log_manager.startup()

    logger_debug = logging.getLogger("cyberdrop_dl_debug")
    import cyberdrop_dl.utils.utilities
    if os.getenv("PYCHARM_HOSTED") is not None or manager.config_manager.settings_data['Runtime_Options']['log_level'] == -1 or 'TERM_PROGRAM' in os.environ.keys() and os.environ['TERM_PROGRAM'] == 'vscode':
        manager.config_manager.settings_data['Runtime_Options']['log_level'] = 10
        cyberdrop_dl.utils.utilities.DEBUG_VAR = True

    if os.getenv("PYCHARM_HOSTED") is not None or manager.config_manager.settings_data['Runtime_Options']['console_log_level'] == -1 or 'TERM_PROGRAM' in os.environ.keys() and os.environ['TERM_PROGRAM'] == 'vscode':
        cyberdrop_dl.utils.utilities.CONSOLE_DEBUG_VAR = True

        
    if cyberdrop_dl.utils.utilities.DEBUG_VAR:
        logger_debug.setLevel(manager.config_manager.settings_data['Runtime_Options']['log_level'])
        if os.getenv("PYCHARM_HOSTED") is not None or 'TERM_PROGRAM' in os.environ.keys() and os.environ['TERM_PROGRAM'] == 'vscode':
            file_handler_debug = logging.FileHandler("../cyberdrop_dl_debug.log", mode="w")
        else:
            file_handler_debug = logging.FileHandler("./cyberdrop_dl_debug.log", mode="w")
        file_handler_debug.setLevel(manager.config_manager.settings_data['Runtime_Options']['log_level'])
        formatter = logging.Formatter("%(levelname)-8s : %(asctime)s : %(filename)s:%(lineno)d : %(message)s")
        file_handler_debug.setFormatter(formatter)
        logger_debug.addHandler(file_handler_debug)

        # aiosqlite_log = logging.getLogger("aiosqlite")
        # aiosqlite_log.setLevel(manager.config_manager.settings_data['Runtime_Options']['log_level'])
        # aiosqlite_log.addHandler(file_handler_debug)

    while True:
        logger = logging.getLogger("cyberdrop_dl")
        if manager.args_manager.all_configs:
            if len(logger.handlers) > 0:
                await log("Picking new config...", 20)

            configs_to_run = list(set(configs) - set(configs_ran))
            configs_to_run.sort()
            manager.config_manager.change_config(configs_to_run[0])
            configs_ran.append(configs_to_run[0])
            if len(logger.handlers) > 0:
                await log(f"Changing config to {configs_to_run[0]}...", 20)
                old_file_handler = logger.handlers[0]
                logger.removeHandler(logger.handlers[0])
                old_file_handler.close()

        logger.setLevel(manager.config_manager.settings_data['Runtime_Options']['log_level'])
        file_handler = logging.FileHandler(manager.path_manager.main_log, mode="w")
        
        if cyberdrop_dl.utils.utilities.DEBUG_VAR:
            manager.config_manager.settings_data['Runtime_Options']['log_level'] = 10
        file_handler.setLevel(manager.config_manager.settings_data['Runtime_Options']['log_level'])

        formatter = logging.Formatter("%(levelname)-8s : %(asctime)s : %(filename)s:%(lineno)d : %(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        import cyberdrop_dl.managers.console_manager
        cyberdrop_dl.managers.console_manager.LEVEL=manager.config_manager.settings_data['Runtime_Options']['console_log_level']

        await log("Starting Async Processes...", 20)
        await manager.async_startup()

        await log("Starting UI...", 20)
        if not manager.args_manager.sort_all_configs:
            try:
                async with manager.live_manager.get_main_live(stop=True) :
                    await runtime(manager)
                    await post_runtime(manager)
            except Exception as e:
                print_("\nAn error occurred, please report this to the developer")
                print_(e)
                print_(traceback.format_exc())
                exit(1)

        clear_screen_proc = await asyncio.create_subprocess_shell('cls' if os.name == 'nt' else 'clear')
        await clear_screen_proc.wait()

        await log_with_color(f"Running Post-Download Processes For Config: {manager.config_manager.loaded_config}...", "green", 20)
        if isinstance(manager.args_manager.sort_downloads, bool):
            if manager.args_manager.sort_downloads:
                sorter = Sorter(manager)
                await sorter.sort()
        elif manager.config_manager.settings_data['Sorting']['sort_downloads'] and not manager.args_manager.retry_any:
            sorter = Sorter(manager)
            await sorter.sort()
        await check_partials_and_empty_folders(manager)
        
        if manager.config_manager.settings_data['Runtime_Options']['update_last_forum_post']:
            await log("Updating Last Forum Post...", 20)
            await manager.log_manager.update_last_forum_post()
            
        
        # add the stuff here

        
        await log("Printing Stats...", 20)
        await manager.progress_manager.print_stats()

        await log("Checking for Program End...", 20)
        if not manager.args_manager.all_configs or not list(set(configs) - set(configs_ran)):
            break
        await asyncio.sleep(5)

    await log("Checking for Updates...", 20)
    await check_latest_pypi()

    await log("Closing Program...", 20)
    await manager.close()

    await log_with_color("\nFinished downloading. Enjoy :)", 'green', 20)


def main():
    manager = startup()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    with contextlib.suppress(RuntimeError):
        try:
            asyncio.run(director(manager))
        except KeyboardInterrupt:
            print_("\nTrying to Exit...")
            with contextlib.suppress(Exception):
                asyncio.run(manager.close())
            exit(1)
    loop.close()
    sys.exit(0)


if __name__ == '__main__':
    main()
