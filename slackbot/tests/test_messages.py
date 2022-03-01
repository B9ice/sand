from pathlib import Path

import pytest

from pages.BasePage import BasePage


class BaseTest(BasePage):
    def test_send_message_on_default_channel(self):
        # for keeping track of how long to wait when searching for a message based
        # qa requirements
        search_wait_time = self.cfg['qa_settings']['search_wait_time']
        msg = self.unique_message()
        assert self.select_channel("general").\
            send_message(msg).\
            save_message(msg), f"could not save '{msg}'"

        assert self.search_saved_messages(msg, refresh=True, wait_time=search_wait_time), \
            f"could not find '{msg}'. search_wait_time = {search_wait_time} secs"


if __name__ == '__main__':
    pytest.main(['--docker-compose', Path(__file__).parent.as_posix(),
                 '--docker-compose-no-build'])