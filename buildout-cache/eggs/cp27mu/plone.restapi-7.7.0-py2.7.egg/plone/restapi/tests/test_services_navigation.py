# -*- coding: utf-8 -*-
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.dexterity.utils import createContentInContainer
from plone.restapi.testing import PLONE_RESTAPI_DX_FUNCTIONAL_TESTING
from plone.restapi.testing import RelativeSession

import transaction
import unittest


try:
    from Products.CMFPlone.factory import _IMREALLYPLONE5  # noqa
except ImportError:
    PLONE5 = False
else:
    PLONE5 = True


class TestServicesNavigation(unittest.TestCase):

    layer = PLONE_RESTAPI_DX_FUNCTIONAL_TESTING

    def setUp(self):
        self.app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.portal_url = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        self.api_session = RelativeSession(self.portal_url)
        self.api_session.headers.update({"Accept": "application/json"})
        self.api_session.auth = (SITE_OWNER_NAME, SITE_OWNER_PASSWORD)

        self.folder = createContentInContainer(
            self.portal, u"Folder", id=u"folder", title=u"Some Folder"
        )
        self.folder2 = createContentInContainer(
            self.portal, u"Folder", id=u"folder2", title=u"Some Folder 2"
        )
        self.subfolder1 = createContentInContainer(
            self.folder, u"Folder", id=u"subfolder1", title=u"SubFolder 1"
        )
        self.subfolder2 = createContentInContainer(
            self.folder, u"Folder", id=u"subfolder2", title=u"SubFolder 2"
        )
        self.thirdlevelfolder = createContentInContainer(
            self.subfolder1,
            u"Folder",
            id=u"thirdlevelfolder",
            title=u"Third Level Folder",
        )
        self.fourthlevelfolder = createContentInContainer(
            self.thirdlevelfolder,
            u"Folder",
            id=u"fourthlevelfolder",
            title=u"Fourth Level Folder",
        )
        createContentInContainer(
            self.folder, u"Document", id=u"doc1", title=u"A document"
        )
        transaction.commit()

    def tearDown(self):
        self.api_session.close()

    @unittest.skipIf(
        not PLONE5,
        "Just Plone 5 currently, tabs in plone 4 does not have review_state",
    )
    def test_navigation_with_no_params_gets_only_top_level(self):
        response = self.api_session.get("/folder/@navigation")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "@id": self.portal_url + u"/folder/@navigation",
                "items": [
                    {
                        u"@id": self.portal_url,
                        u"description": u"",
                        u"items": [],
                        u"review_state": None,
                        u"title": u"Home",
                    },
                    {
                        u"@id": self.portal_url + u"/folder",
                        u"description": u"",
                        u"items": [],
                        u"review_state": "private",
                        u"title": u"Some Folder",
                    },
                    {
                        u"@id": self.portal_url + u"/folder2",
                        u"description": u"",
                        u"items": [],
                        u"review_state": "private",
                        u"title": u"Some Folder 2",
                    },
                ],
            },
        )

    def test_navigation_service(self):
        response = self.api_session.get(
            "/folder/@navigation", params={"expand.navigation.depth": 2}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["items"]), 3)
        self.assertEqual(response.json()["items"][1]["title"], u"Some Folder")
        self.assertEqual(len(response.json()["items"][1]["items"]), 3)
        self.assertEqual(len(response.json()["items"][2]["items"]), 0)

        response = self.api_session.get(
            "/folder/@navigation", params={"expand.navigation.depth": 3}
        )

        self.assertEqual(len(response.json()["items"][1]["items"][0]["items"]), 1)
        self.assertEqual(
            response.json()["items"][1]["items"][0]["items"][0]["title"],
            u"Third Level Folder",
        )
        self.assertEqual(
            len(response.json()["items"][1]["items"][0]["items"][0]["items"]),
            0,
        )

        response = self.api_session.get(
            "/folder/@navigation", params={"expand.navigation.depth": 4}
        )

        self.assertEqual(
            len(response.json()["items"][1]["items"][0]["items"][0]["items"]),
            1,
        )
        self.assertEqual(
            response.json()["items"][1]["items"][0]["items"][0]["items"][0][
                "title"
            ],  # noqa
            u"Fourth Level Folder",
        )

    def test_dont_broke_with_contents_without_review_state(self):
        createContentInContainer(
            self.portal,
            u"File",
            id=u"example-file",
            title=u"Example file",
        )
        createContentInContainer(
            self.folder,
            u"File",
            id=u"example-file-1",
            title=u"Example file 1",
        )
        transaction.commit()

        response = self.api_session.get("/folder/@navigation")
        self.assertIsNone(response.json()["items"][3]["review_state"])

        response = self.api_session.get(
            "/folder/@navigation", params={"expand.navigation.depth": 2}
        )
        self.assertIsNone(response.json()["items"][1]["items"][3]["review_state"])

    def test_navigation_sorting(self):
        createContentInContainer(
            self.portal,
            u"File",
            id=u"example-file",
            title=u"Example file",
        )
        createContentInContainer(
            self.folder,
            u"File",
            id=u"example-file-1",
            title=u"Example file 1",
        )
        transaction.commit()
        response = self.api_session.get(
            "/folder/@navigation", params={"expand.navigation.depth": 2}
        ).json()

        contents = response["items"][1]["items"]
        self.assertEqual(
            [p["@id"].replace(self.portal.absolute_url(), "") for p in contents],
            [
                "/folder/subfolder1",
                "/folder/subfolder2",
                "/folder/doc1",
                "/folder/example-file-1",
            ],
        )

        self.portal["folder"].moveObjectsUp(["example-file-1"])
        transaction.commit()
        response = self.api_session.get(
            "/folder/@navigation", params={"expand.navigation.depth": 2}
        ).json()
        contents = response["items"][1]["items"]
        self.assertEqual(
            [p["@id"].replace(self.portal.absolute_url(), "") for p in contents],
            [
                "/folder/subfolder1",
                "/folder/subfolder2",
                "/folder/example-file-1",
                "/folder/doc1",
            ],
        )
