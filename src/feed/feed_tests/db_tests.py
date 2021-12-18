from lib.test import TestCase
from lib.models import User
from src.feed.models import *
from src.feed.services.db_services import *


class FeedGettingTests(TestCase):
    async def setUp(self):
        self.user = await User.create_user(username='TestUser', password='TestUserPassword')
        self.feed_post = await FeedPost.create(author=self.user, text='Test text')

        self.feed_post_image = await FeedPostImage.create()

        self.feed_post_comment = await FeedPostComment.create(author=self.user, text='Test comment text')

        self.feed_post_like = await FeedPostLike.create(author=self.user)

    async def test_get_feed_post_by_params(self):
        self.assertEquals(self.feed_post, await get_feed_post_by_params(id=self.feed_post.id),
                          msg='get_feed_post_by_params <feed.services.db_services> returned '
                              'the wrong feed post <feed.models.FeedPost>')

    async def test_get_feed_post_image_by_params(self):
        self.assertEquals(self.feed_post_image, await get_feed_post_image_by_params(id=self.feed_post_image.id),
                          msg='get_feed_post_image_by_params <feed.services.db_services> returned'
                              'the wrong feed image <feed.models.FeedPostImage')

    async def test_get_feed_post_comment_by_params(self):
        self.assertEquals(self.feed_post_comment, await get_feed_post_comment_by_params(id=self.feed_post_comment.id),
                          msg='get_feed_post_comment_by_params <feed.services.db_services> returned'
                              'the wrong feed comment <feed.models.FeedPostComment')

    async def test_get_feed_post_like_by_params(self):
        self.assertEquals(self.feed_post_like, await get_feed_post_like_by_params(id=self.feed_post_like.id),
                          msg='get_feed_post_like_by_params <feed.services.db_services> returned'
                              'the wrong feed like <feed.models.FeedPostLike>')


class FeedCreatingTests(TestCase):
    async def setUp(self):
        self.user = await User.create_user(username='TestUser', password='TestUserPassword')
        self.image_file = open('src/feed/feed_tests/test_image.png', 'rb')

    async def test_create_feed_post_image(self):
        image = await create_feed_post_image(self.image_file)
        self.assertTrue(isinstance(image, FeedPostImage),
                        msg='create_feed_post_image <feed.services.db_services> '
                            'had not created feed post image <feed.models.FeedPostImage>')
        self.assertEquals(image, await get_feed_post_image_by_params(id=image.id),
                          msg='create_feed_post_image <feed.services.db_services> '
                              'had not saved feed post image <feed.models.FeedPostImage>')

    async def test_create_feed_post(self):
        image = await create_feed_post_image(self.image_file)
        post = await create_feed_post(author=self.user, text='Test feed post text', images=(image,))
        self.assertTrue(isinstance(post, FeedPost),
                        msg='create_feed_post <feed.services.db_services>'
                            'had not created feed post <feed.models.FeedPost>')
        self.assertEquals(post, await get_feed_post_by_params(id=post.id))

    async def test_create_feed_post_comment(self):
        comment = await create_feed_post_comment(self.user, 'Test feed post comment')
        self.assertTrue(isinstance(comment, FeedPostComment),
                        msg='create_feed_post_comment <feed.services.db_services>'
                            'had not created feed post comment <feed.models.FeedPostComment>')
        self.assertEquals(comment, await get_feed_post_comment_by_params(id=comment.id))


class FeedAddingTests(TestCase):
    async def setUp(self):
        self.user = await User.create_user(username='TestUser', password='TestUserPassword')

    async def test_add_like_to_feed_post(self):
        post = await create_feed_post(self.user, 'Test adding like to feed post')
        await add_like_to_feed_post(post, self.user)
        self.assertEquals(await post.likes.all().count(), 1,
                          msg='add_like_to_feed_post <feed.services.db_services>'
                              'had not added like to post <feed.models.FeedPost>')
        await remove_like_from_feed_post(post, self.user)
        self.assertEquals(await post.likes.all().count(), 0,
                          msg='remove_like_from_feed_post <feed.services.db_services>'
                              'had not removed like from post <feed.models.FeedPost>')

    async def test_add_comment_to_feed_post(self):
        post = await create_feed_post(self.user, 'Test adding comment to feed post')
        comment = await create_feed_post_comment(self.user, 'Test comment')
        result = await add_comment_to_feed_post(post, comment)
        self.assertTrue(comment in await post.comments.all(),
                          msg='add_comment_to_feed_post <feed.services.db_services'
                              'had not added comment to post <feed.models.FeedPost>')
