from .about import about_view
from .brands import brand_create_view, brand_detail_view
from .candles import CandleList_view, candle_list_view, candle_detail_view, candle_create_view, candle_experience_vote_create_view, candle_experience_vote_update_view
from .front_page import home_screen_view, frontpage_view
from .lists import listiem_add_create_view, listitem_delete_view
from .profiles import profile_view
from .redirectpreviousmixin import RedirectToPreviousMixin
from .reports import report_review_create_view
from .reviews import ReviewList_view, review_list_view, review_candle_create_view, review_candle_update_view, review_candle_delete_view
from .search import candle_filter_search
from .likes_and_notifications import reviewlike_create_view, notifications_view

__all__ = [
    'about_view',
    'brand_create_view',
    'brand_detail_view',
    'CandleList_view',
    'candle_list_view',
    'candle_detail_view',
    'candle_create_view',
    'candle_experience_vote_create_view',
    'candle_experience_vote_update_view',
    'home_screen_view',
    'frontpage_view',
    'listiem_add_create_view',
    'listitem_delete_view',
    'profile_view',
    'report_review_create_view',
    'ReviewList_view',
    'review_list_view',
    'review_candle_create_view',
    'review_candle_update_view',
    'review_candle_delete_view',
    'candle_filter_search',
    'reviewlike_create_view',
    'notifications_view',
]
