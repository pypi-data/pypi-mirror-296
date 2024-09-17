from uuid import uuid4

import conftest
from botcity.plugins.googledrive import BotGoogleDrivePlugin

import os

def test_return_correct_file_id(bot: BotGoogleDrivePlugin, create_folder: str, tmp_folder: str):
    file_id = conftest.create_file_in_google_drive(bot=bot, file_name="Test Txt One", parent_folder_id=create_folder, file_type="txt",
                                         tmp_folder=tmp_folder, mimetype="text/plain")
    search_file_id = bot.search_file_by_name("Test Txt One")
    assert file_id == search_file_id


def test_return_none_for_non_existent_file(bot: BotGoogleDrivePlugin):
    file_id = bot.search_file_by_name("file.txt")
    assert file_id is None


def test_create_folder(bot: BotGoogleDrivePlugin, create_folder: str):
    folder_name = str(uuid4())
    created_folder_id = bot.create_folder(folder_name=folder_name, parent_folder_id=create_folder)
    assert isinstance(created_folder_id, str)


def test_return_correct_folder_id(bot: BotGoogleDrivePlugin, create_folder: str):
    folder_id = bot.search_folder_by_name(folder_name=conftest.FOLDER_NAME)
    assert folder_id == create_folder


def test_return_none_for_non_existent_folder(bot: BotGoogleDrivePlugin):
    folder_id = bot.search_folder_by_name("Pasta 2 - Testes")
    assert folder_id is None


def test_upload_file(bot: BotGoogleDrivePlugin, create_folder: str, tmp_folder: str):
    conftest.create_file_in_google_drive(bot=bot, file_name="Test Upload File", parent_folder_id=create_folder, file_type="txt",
                                         tmp_folder=tmp_folder, mimetype="text/plain")
    search_file_id = bot.search_file_by_name("Test Upload File")
    assert isinstance(search_file_id, str)


def test_search_file_support_all_drives_active(bot: BotGoogleDrivePlugin, create_folder: str, tmp_folder: str):
    bot.support_all_drives = True
    search_file_id = bot.search_file_by_name("Test Upload File")
    bot.support_all_drives = False
    assert isinstance(search_file_id, str)


def test_download_file(bot: BotGoogleDrivePlugin, tmp_folder: str):
    file_path = f"{tmp_folder}/Test Upload File.txt"
    os.remove(file_path)
    search_file_id = bot.search_file_by_name("Test Upload File")

    bot.download_file(file_id=search_file_id, file_path=file_path)
    assert os.path.isfile(file_path) == True


def test_return_all_files_from_parent_folder(bot: BotGoogleDrivePlugin, create_folder: str):
    subfiles = bot.get_files_from_parent_folder(create_folder)
    assert len(subfiles) == 3


def test_return_all_files_from_parent_folder_include_filename(bot: BotGoogleDrivePlugin, create_folder: str):
    subfiles = bot.get_files_from_parent_folder(create_folder, include_filename=True)
    assert len(subfiles) == 3 and isinstance(subfiles[0], tuple) and len(subfiles[0]) == 2

def test_do_not_return_any_files_for_empty_folders(bot: BotGoogleDrivePlugin, create_folder: str):
    create_folder_null = bot.create_folder(folder_name="Null Folder", parent_folder_id=create_folder)
    subfiles = bot.get_files_from_parent_folder(create_folder_null)
    assert len(subfiles) == 0
