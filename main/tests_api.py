import uuid

from django.contrib.auth.models import Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from main.models import Project, Experience


class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.project = Project.objects.create(
            title="Portfolio", description="My website", tech_stack="Django",
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "title": "New project", "description": "A useful app", "tech_stack": "Python",
            "project_url": "https://example.com/", "project_image_url": "",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"project_url": "javascript:alert(1)"}, "project_url"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, "My website")
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_staff_without_editor_group_cannot_write(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_editor_can_patch_and_put(self):
        group, _ = Group.objects.get_or_create(name="Editor")
        self.visitor.groups.add(group)
        self.client.force_authenticate(user=self.visitor)

        response = self.client.patch(self.detail_url, {"title": "Edited"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Edited")

        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_editor_cannot_create_or_delete(self):
        group, _ = Group.objects.get_or_create(name="Editor")
        self.visitor.groups.add(group)
        self.client.force_authenticate(user=self.visitor)

        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_get_and_options_do_not_change_data(self):
        for url in (self.list_url, self.detail_url):
            self.assertEqual(self.client.get(url).status_code, status.HTTP_200_OK)
            self.assertEqual(self.client.options(url).status_code, status.HTTP_200_OK)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        # The Browsable API form renders a real CSRF token into the response.
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        

class ExperienceAPITestBase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.password = "pass12345"
        cls.regular = User.objects.create_user("regular", password=cls.password)
        cls.editor = User.objects.create_user("editor", password=cls.password)
        cls.owner = User.objects.create_superuser(
            "owner", "owner@example.com", cls.password
        )
        editor_group, _ = Group.objects.get_or_create(name="Editor")
        cls.editor.groups.add(editor_group)

        cls.experience = Experience.objects.create(
            title="Original title",
            description="Original description",
            category="volunteer",
            started_at="2024-01-01T00:00:00Z",
        )

    def payload(self, **overrides):
        data = {
            "title": "New experience",
            "description": "Something",
            "category": "research",
            "thumbnail": "",
            "started_at": "2024-01-01T00:00:00Z",
            "ended_at": None,
        }
        data.update(overrides)
        return data

    @property
    def list_url(self):
        return reverse("api:experience-list")

    def detail_url(self, pk=None):
        return reverse("api:experience-detail", args=[pk or self.experience.pk])

    def star_url(self, pk=None):
        return reverse("api:experience-star", args=[pk or self.experience.pk])
    
class WritePermissionDeniedTests(ExperienceAPITestBase):
    def assert_nothing_changed(self):
        self.assertEqual(Experience.objects.count(), 1)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Original title")

    def test_visitor_cannot_create(self):
        response = self.client.post(self.list_url, self.payload(), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assert_nothing_changed()

    def test_visitor_cannot_patch_or_delete(self):
        patch = self.client.patch(
            self.detail_url(), {"title": "Hacked"}, format="json"
        )
        delete = self.client.delete(self.detail_url())
        self.assertEqual(patch.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(delete.status_code, status.HTTP_403_FORBIDDEN)
        self.assert_nothing_changed()

    def test_regular_user_cannot_write(self):
        self.client.force_authenticate(self.regular)
        responses = [
            self.client.post(self.list_url, self.payload(), format="json"),
            self.client.patch(self.detail_url(), {"title": "Hacked"}, format="json"),
            self.client.delete(self.detail_url()),
        ]
        for response in responses:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assert_nothing_changed()

    def test_visitor_can_read(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
class RoleTests(ExperienceAPITestBase):
    def test_editor_can_patch(self):
        self.client.force_authenticate(self.editor)
        response = self.client.patch(
            self.detail_url(), {"title": "Edited by editor"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.experience.refresh_from_db()
        self.assertEqual(self.experience.title, "Edited by editor")

    def test_editor_cannot_create(self):
        self.client.force_authenticate(self.editor)
        response = self.client.post(self.list_url, self.payload(), format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

    def test_editor_cannot_delete(self):
        self.client.force_authenticate(self.editor)
        response = self.client.delete(self.detail_url())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())

    def test_owner_can_create(self):
        self.client.force_authenticate(self.owner)
        response = self.client.post(self.list_url, self.payload(), format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Experience.objects.count(), 2)
        self.assertTrue(Experience.objects.filter(title="New experience").exists())

    def test_owner_can_delete(self):
        self.client.force_authenticate(self.owner)
        response = self.client.delete(self.detail_url())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Experience.objects.filter(pk=self.experience.pk).exists())
        
class ValidationTests(ExperienceAPITestBase):
    def setUp(self):
        self.client.force_authenticate(self.owner)

    def test_blank_title_is_rejected(self):
        response = self.client.post(
            self.list_url, self.payload(title="   "), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)
        self.assertEqual(Experience.objects.count(), 1)

    def test_title_with_only_tags_is_rejected(self):
        response = self.client.post(
            self.list_url, self.payload(title="<b></b>"), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Experience.objects.count(), 1)

    def test_html_tags_are_stripped_before_saving(self):
        response = self.client.post(
            self.list_url,
            self.payload(
                title="<script>x</script>Safe",
                description="<b>bold</b> text",
            ),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        saved = Experience.objects.get(pk=response.data["id"])
        self.assertNotIn("<", saved.title)
        self.assertEqual(saved.description, "bold text")

    def test_ongoing_experience_without_end_date_is_valid(self):
        response = self.client.post(
            self.list_url, self.payload(ended_at=None), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_end_date_before_start_date_is_rejected(self):
        # hanya lolos kalau kamu sudah menambah validate() di serializer
        response = self.client.post(
            self.list_url,
            self.payload(
                started_at="2024-06-01T00:00:00Z",
                ended_at="2024-01-01T00:00:00Z",
            ),
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Experience.objects.count(), 1)
        
class StarTests(ExperienceAPITestBase):
    def test_visitor_cannot_star(self):
        response = self.client.post(self.star_url())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_user_can_star_and_unstar(self):
        self.client.force_authenticate(self.regular)

        first = self.client.post(self.star_url())
        self.assertEqual(first.status_code, status.HTTP_200_OK)
        self.assertTrue(first.data["is_starred"])
        self.assertEqual(first.data["star_count"], 1)
        self.assertTrue(self.experience.starred_by.filter(pk=self.regular.pk).exists())

        second = self.client.post(self.star_url())
        self.assertFalse(second.data["is_starred"])
        self.assertEqual(second.data["star_count"], 0)
        self.assertEqual(self.experience.starred_by.count(), 0)

    def test_star_uses_logged_in_user_not_request_body(self):
        self.client.force_authenticate(self.regular)
        self.client.post(self.star_url(), {"user": self.owner.pk}, format="json")
        starrers = list(self.experience.starred_by.all())
        self.assertEqual(starrers, [self.regular])

    def test_star_unknown_experience_returns_404(self):
        self.client.force_authenticate(self.regular)
        response = self.client.post(
            self.star_url("00000000-0000-0000-0000-000000000000")
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_star_response_hides_sensitive_account_data(self):
        self.client.force_authenticate(self.regular)
        response = self.client.post(self.star_url())
        self.assertNotIn("email", str(response.data))
        self.assertNotIn("password", str(response.data))
        
class CSRFTests(ExperienceAPITestBase):
    def test_write_without_csrf_token_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password=self.password))

        response = client.post(self.list_url, self.payload(), format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Experience.objects.count(), 1)

    def test_delete_without_csrf_token_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password=self.password)

        response = client.delete(self.detail_url())

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Experience.objects.filter(pk=self.experience.pk).exists())