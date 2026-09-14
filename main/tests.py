from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from main.models import Experience, Skill


class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="Asisten Dosen PBP",
            description="Membantu mahasiswa memahami pengembangan web.",
            category="part-time",
        )
        
        self.skill = Skill.objects.create(
            title="Time Traveling",
            description="Mampu menjelajahi berbagai masa di bumi terbatas pada 5 abad sebelum dan 3 abad setelah dengan constraint tidak dapat menjelajahi lebih dari satu minggu setiap perjalanannya.",
            category="hard",
            gained_from = "Self-taught",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertNotContains(response, self.skill.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')
        self.assertContains(response, f'href="{reverse("main:show_skill")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/halaman-yang-tidak-ada/")

        self.assertEqual(response.status_code, 404)
        
    # Model Test
    def test_experience_model(self):
        self.assertEqual(str(self.experience), "Asisten Dosen PBP")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)
        
    def test_skill_model(self):
        self.assertEqual(str(self.skill), "Time Traveling")
        self.assertEqual(self.skill.category, "hard")
        self.assertTrue(self.skill.gained_from, "Self-taught")

    # Page test
    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Sedang berlangsung")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')
        self.assertContains(response, f'href="{reverse("main:show_skill")}"')
        
    def test_experience_page(self):
            response = self.client.get(reverse("main:show_skill"))
    
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "skill.html")
            self.assertContains(response, self.skill.title)
            self.assertContains(response, self.skill.description)
            self.assertContains(response, self.skill.gained_from)
            self.assertContains(response, "Hard skill")
            self.assertContains(response, f'href="{reverse("main:show_main")}"')
            self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "Belum ada pengalaman yang ditambahkan.")

    def test_empty_skill_page(self):
            Skill.objects.all().delete()
            response = self.client.get(reverse("main:show_skill"))
    
            self.assertContains(response, "Belum ada skill yang ditambahkan.")
            
    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Selesai")
        self.assertNotContains(response, "Sedang berlangsung")