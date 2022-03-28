import pytest

from pages.BasePage import BasePage


class BaseTest(BasePage):
    def test_search_text_max_length(self):
        max_len = 256
        valid_expected_f = f"We couldn’t find any repositories matching '%s'"
        invalid_expected = "The search is longer than 256 characters"

        valid_text_255 = '#' * (max_len - 1)
        self.search(valid_text_255)
        assert self.text_exists(valid_expected_f % valid_text_255), 'unexpected response for search text of len(255)'

        valid_text_256 = '#' * max_len
        self.search(valid_text_256)
        assert self.text_exists(valid_expected_f % valid_text_256), 'unexpected response for search text of len(256)'

        invalid_text_257 = '#' * (max_len + 1)
        self.search(invalid_text_257)
        assert self.text_exists(invalid_expected), 'unexpected response for search text of len(257)'

    def test_search_random_special_characters(self):
        q = '####@@@##,*^'
        expected_text = f"We couldn’t find any repositories matching '{q}'"

        self.search(q)
        assert self.text_exists(expected_text)

    def test_search_random_alpha_numeric(self):
        q = '1290hsraaorandaAthenIINE44495_'
        expected_text = f"We couldn’t find any repositories matching '{q}'"

        self.search(q)
        assert self.text_exists(expected_text)

    def test_advanced_search_prefixes(self):
        q = 'react stars:>45 followers:>50 language:JavaScript license:bsl-1.0 state:closed'
        self.search(q)

        assert self.text_exists("1 repository result")
        assert self.link_exists("mvoloskov/decider")

    def test_advanced_search(self):
        # search reach
        self.search('react')
        # enter advanced search stars fields
        self.advanced_search_field(
            **self.cfg['locators']['search']['stars'],
            submit=False
        )
        # enter advanced search followers fields
        self.advanced_search_field(
            **self.cfg['locators']['search']['user']['followers'],
            submit=False
        )
        # select advanced search language option
        self.advanced_search_options(
            options=self.cfg['locators']['search']['user']['language'],
            option=self.cfg['locators']['search']['user']['language']['option'],
            submit=False
        )
        # select advanced issue state (open/close) option
        self.advanced_search_options(
            options=self.cfg['locators']['search']['issues'],
            option=self.cfg['locators']['search']['issues']['state'],
            submit=False
        )
        # select advanced search license option
        self.advanced_search_options(
            options=self.cfg['locators']['search']['license'],
            option=self.cfg['locators']['search']['license']['option'],
            submit=True
        )

        assert self.text_exists("1 repository result")
        assert self.link_exists("mvoloskov/decider")


if __name__ == '__main__':
    pytest.main()
    # pytest.main(['--docker-compose', Path(__file__).parent.parent.as_posix(),
                  # '--docker-compose-no-build'])