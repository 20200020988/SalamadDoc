![SALAMADOC LOGO](https://github.com/2202-XU-CSCC22A/groupB/assets/124771373/11d34848-5757-4a19-bba3-28d1db8c0543)

# Salamadoc: Management Appointment Web App System

Welcome to the SALAMADOK web application! This application allows patients, admins, doctors, and secretaries to manage appointments and user information. Below is a brief guide on how to use the application for each user role.


## Features

### Patient
- **Create an Appointment**

    You can schedule an appointment with a doctor of your choice. Provide the necessary details such as the doctor's specialty, appointment date, and the reason for the appointment.

- **View Appointments**

    You can see your upcoming and past appointments. The information displayed includes the doctor's name, specialty, and the appointment date.

- **View Doctors**

    You can the list of doctors available. The information displayed includes the doctor's name, specialty, and contact info.

### Doctor
- **View Appointments**

    Through the dashboard, you can see the appointments set by patients/customers. This allows you to view the tentative appointment schedules and details of each appointment.

- **Edit Appointments**

    Doctors have the ability to modify details of existing appointments, such as canceling appointments as needed.

- **View Patients**

    Doctors can access patient records and medical history, allowing them to review important information about their patients.


- **Assign Departments/Specialty**

    Doctors can be assigned to specific departments or specialties, which helps in categorizing and organizing the medical staff.

- **Assign Secretary**

    Doctors can assign a secretary to assist them with administrative tasks, such as managing appointments, handling patient inquiries, and organizing paperwork.

### Secretary

- **View Appointments of the Linked Doctor**

    Secretaries can access and view the appointments of the doctor they are linked to. This enables them to stay informed about the doctor's schedule and assist with appointment management.

- **Edit Appointments of the Linked Doctor**

    Secretaries have the ability to make changes to appointments of the doctor they are linked to, such as canceling appointments based on the doctor's instructions.

### Admin
- **View Groups**

    You can see a list of available groups in the application, including admin, doctor, patient, and secretary. This section also provides information about the permissions associated with each role.

- **View Users**

    You can view the user information of the web application, including the username, email address, first name, and last name. This helps in managing user accounts and their details.
    

## Screenshots

- Patient's Dashboard
    ![Patient_Dashboard](https://github.com/2202-XU-CSCC22A/groupB/assets/124771373/a46118f0-1f3d-4994-be96-369a58f55cfe)

- Doctor's Dashboard
    ![Doctor_Dashboard](https://github.com/2202-XU-CSCC22A/groupB/assets/124771373/94e29c6d-5479-4b31-8b22-4a5f48bf26cc)

- Admin's Dashboard
    ![Admin_Dashboard](https://github.com/2202-XU-CSCC22A/groupB/assets/124771373/5adcc6b9-3f91-49a9-9703-48515aeb5204)
    

## Run Locally

Clone the project

```bash
  git clone https://github.com/2202-XU-CSCC22A/groupB
```

Go to the project directory

```bash
  cd myproject
```

Start the server

```bash
  py manage.py runserver
```

## Acknowledgements

 - [PolluxUI](https://github.com/BootstrapDash/polluxui-free-admin-template)
 - [Django](https://www.djangoproject.com/)
 - [SQLite](https://www.sqlite.org/index.html)
