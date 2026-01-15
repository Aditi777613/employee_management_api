from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Employee

class EmployeeTests(APITestCase):
    def setUp(self):
        # Create user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        
        # Create sample employee
        self.employee_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'department': 'Engineering',
            'role': 'Developer'
        }
        self.employee = Employee.objects.create(**self.employee_data)
        self.url = reverse('employee-list')

    def test_create_employee(self):
        new_employee = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'department': 'HR',
            'role': 'Manager'
        }
        response = self.client.post(self.url, new_employee)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 2)

    def test_create_employee_duplicate_email(self):
        response = self.client.post(self.url, self.employee_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_employees(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check pagination structure or result count
        # DRF default pagination returns { "count": ..., "next": ..., "previous": ..., "results": [...] }
        self.assertEqual(len(response.data['results']), 1)

    def test_retrieve_employee(self):
        url = reverse('employee-detail', args=[self.employee.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.employee.email)

    def test_update_employee(self):
        url = reverse('employee-detail', args=[self.employee.id])
        updated_data = {'name': 'John Updated', 'email': 'john@example.com'}
        response = self.client.patch(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.name, 'John Updated')

    def test_delete_employee(self):
        url = reverse('employee-detail', args=[self.employee.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(), 0)

    def test_unauthenticated_access(self):
        self.client.logout()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
