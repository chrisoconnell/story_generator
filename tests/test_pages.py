from story_generator.pages import get_html, get_path_to_summaries, get_path_to_stories, get_summary_pages, get_story_page_from_summary_page, \
    get_list_of_summary_pages, get_chapters_from_page
import pytest
from bs4 import BeautifulSoup
import os.path
from unittest.mock import mock_open, patch


def test_get_html():
    result = get_html("Test Page", "Test Content")
    soup = BeautifulSoup(result, 'html.parser')
    # Check required elements
    assert soup.html is not None
    assert soup.head is not None
    assert soup.title is not None
    assert soup.body is not None

def test_get_path_to_summaries():
    result = get_path_to_summaries()
    assert os.path.basename(result) == 'summaries'
    assert os.path.isabs(result)

    result = get_path_to_summaries('test')
    assert os.path.isabs(result)
    assert result.endswith(f'summaries{os.path.sep}test')


def test_get_path_to_stories():
    result = get_path_to_stories()
    assert os.path.basename(result) == 'stories'
    assert os.path.isabs(result)

    result = get_path_to_stories('test')
    assert os.path.isabs(result)
    assert result.endswith(f'stories{os.path.sep}test')

def test_get_summary_pages():
    result = get_summary_pages('Example')
    assert isinstance(result, list)

def test_get_story_page_from_summary_page():
    result = get_story_page_from_summary_page('page1.txt')
    assert result == 'page1.htm'

def test_get_list_of_summary_pages():
    result = get_list_of_summary_pages('Example')
    assert isinstance(result, list)


@pytest.fixture
def mock_file_data():
    return """  Chapter 1: Beginning
Chapter 2: Middle 


  Chapter 3: End 

"""

def test_get_chapters_from_page(mock_file_data):
    with patch('builtins.open', mock_open(read_data=mock_file_data)):
        result = get_chapters_from_page('Example', 'page1.txt')
        assert result == ['Chapter 1: Beginning', 'Chapter 2: Middle', 'Chapter 3: End']
