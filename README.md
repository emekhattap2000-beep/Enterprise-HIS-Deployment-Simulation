# 🏥 Enterprise Hospital Information System (HIS) Deployment & Simulation

## 📖 Overview
A comprehensive infrastructure design, modular deployment, and high-stress volume simulation of an enterprise-level medical management system (Bahmni/OpenMRS). This project demonstrates full-stack DevOps capabilities, from database architecture and synthetic data generation to Docker microservices deployment and system security.

## 🛠️ Tech Stack
* **Infrastructure:** Docker, Docker-Compose, Linux/Ubuntu (WSL)
* **Database:** MySQL / MariaDB
* **Scripting & Automation:** Python (pyodbc, Faker, random), Bash Scripting, Cron
* **System Architecture:** Bahmni / OpenMRS, Role-Based Access Control (RBAC)

## 🧬 Key Features & Methodology

### 1. High-Stress Database Simulation
* Architected a robust relational database schema (`MySQL/MariaDB`) designed for enterprise medical records.
* Engineered advanced Python automation scripts using `pyodbc` and `Faker` to synthesize **500,000+ realistic medical, financial, and demographic records**.
* Used this dataset to perform rigorous performance stress testing on the database architecture.

### 2. Modular Deployment Architecture
* Built and configured a local, self-hosted web environment via **Docker Microservices** (`docker-compose`).
* Established adaptive environments allowing independent configurations for:
  * Full hospital networks
  * Dental-only clinics
  * Isolated laboratory networks

### 3. Security & System Maintenance
* Designed an end-to-end operational manual ensuring HIPAA-like security standards.
* Implemented secure **Role-Based Access Control (RBAC)** to restrict system access based on user roles.
* Configured daily automated backup routines using **Bash scripting & Cron jobs**.
* Set up comprehensive audit logging tracking and local network firewall rules.

## 🚀 How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/emekhattap2000/Enterprise-HIS-Deployment-Simulation.git
   ```
2. Install Python dependencies for data generation:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the synthetic data generator:
   ```bash
   python scripts/data_generator.py
   ```
4. Start the Docker microservices:
   ```bash
   cd docker
   docker-compose up -d
   ```

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

Click the green **"Commit changes"** button to save your README.

---

### Step 5: Pin the Project to Your Profile
1. Go to your main GitHub profile page (`github.com/emekhattap2000`).
2. Click **"Customize your pins"**.
3. Make sure both `ML-Physical-Performance-Classification` and `Enterprise-HIS-Deployment-Simulation` are selected.
4. Click **Save**.
