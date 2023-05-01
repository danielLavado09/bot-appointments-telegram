class DBManager:
    def __init__(self, conn):
        self.conn = conn

    def create_users_table(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS Users (
            user_id INT NOT NULL,
            id TEXT NOT NULL,
            name TEXT NOT NULL,
            age INT NOT NULL,
            email TEXT NOT NULL,
            cellphone TEXT NOT NULL,
            PRIMARY KEY (user_id))''')
        self.conn.commit()

    def create_appointments_table(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS Appointments (
            appointment_id TEXT NOT NULL,
            user_id INT NOT NULL,
            doctor_id TEXT NOT NULL,
            specialty TEXT NOT NULL,
            date_due DATE NOT NULL,
            PRIMARY KEY (appointment_id),
            FOREIGN KEY (doctor_id, specialty)
                REFERENCES Doctors(doctor_id, specialty)
                ON DELETE CASCADE
                ON UPDATE CASCADE,
            FOREIGN KEY (user_id)
                REFERENCES Users(user_id)
                ON DELETE CASCADE
                ON UPDATE CASCADE)''')
        self.conn.commit()

    def create_doctors_table(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS Doctors (
            doctor_id TEXT NOT NULL,
            id INT NOT NULL,
            name TEXT NOT NULL,
            specialty TEXT NOT NULL,
            PRIMARY KEY (doctor_id))''')
        self.conn.commit()

    def validate_user(self, user_id):
        c = self.conn.cursor()
        c.execute("SELECT user_id FROM Users WHERE user_id=?", (user_id,))
        result = c.fetchone()

        return bool(result)

    def register_user(self, user_id, id, name, age, email, cellphone):
        c = self.conn.cursor()
        c.execute("INSERT INTO Users (user_id, id, name, age, email, cellphone) VALUES (?, ?, ?, ?, ?, ?)",
                  (user_id, id, name, age, email, cellphone))
        self.conn.commit()

    def get_appointments(self, user_id):
        c = self.conn.cursor()
        c.execute(
            "SELECT * FROM Appointments WHERE user_id=? ORDER BY date_due DESC", (user_id,))
        results = c.fetchall()

        appointments = [result[4] for result in results if not result[3]]

        return appointments

    def get_user_name(self, user_id):
        c = self.conn.cursor()
        c.execute("SELECT name FROM Users WHERE user_id=?", (user_id,))
        result = c.fetchone()

        if result:
            return result[0]
        else:
            return None

    def get_specialties(self):
        c = self.conn.cursor()
        c.execute("SELECT DISTINCT specialty FROM Doctors")
        result = c.fetchall()

        specialties = [result[0] for result in result]

        return specialties

    def get_doctors_by_specialties(self, specialty):
        c = self.conn.cursor()
        c.execute("SELECT name, doctor_id FROM Doctors WHERE specialty=?", (specialty,))
        result = c.fetchall()

        return result

    def validate_user_date(self, user_id, date_due):
        c = self.conn.cursor()
        c.execute("SELECT * FROM Appointments WHERE user_id=? AND date_due=?", (user_id, date_due,))
        result = c.fetchone()

        return bool(result)

    def validate_doctor_agenda(self, doctor_id, date_due):
        c = self.conn.cursor()
        c.execute('''SELECT doctor_id, date_due, COUNT(*) as num_doctors
                        FROM Appointments
                        GROUP BY doctor_id, date_due
                        HAVING num_doctors >= 5''')
        result = c.fetchall()
        if len(result) > 0:
            return True
        else:
            return False

    def register_appointment(self, appointment_id, user_id, doctor_id, specialty, date_due):
        c = self.conn.cursor()
        c.execute('''INSERT INTO Appointments (
                        appointment_id, user_id, doctor_id, specialty, date_due) 
                        VALUES (?, ?, ?, ?, ?)''', (appointment_id, user_id, doctor_id, specialty, date_due))

        self.conn.commit()
