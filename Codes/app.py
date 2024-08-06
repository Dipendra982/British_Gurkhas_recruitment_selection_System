from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import customtkinter as ctk
from threading import Thread
import sqlite3 as db
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Initialize database and create user table if it doesn't exist
def initialize_database():
    try:
        conn = db.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS user(
                    username TEXT PRIMARY KEY,
                    password TEXT,
                    name_1 TEXT,
                    dob_1 TEXT,
                    phone_1 TEXT
                )
            """
        )
        conn.commit()
    except db.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        conn.close()

# Thread for opening register frame because it takes time to load
def threading():
    main_Frame.destroy()
    t1 = Thread(target=open_register)
    t1.start()
    main_Frame.destroy()
 
# Thread for opening login frame because it takes time to load
def threading2():
    main_Frame.destroy()
    t2= Thread(target=create_login_frame)
    t2.start()

# main window
root = Tk()
root.title("British Gurkhas recruitment process")
root.maxsize(1280, 832)
root.minsize(1280, 832)

background = "#2D8A69"
framefg = "white"
frame_clr = "#DBDBDB"

font1 = ("Arial", 20)
font2 = ("Trebuchet MS", 15, "bold")
font3 = ("Trebuchet MS", 50, "bold")

font1 = ("Arial", 20) # for the entry fields, buttons
logout_font = ("Trebuchet MS", 15, "bold") # for the forget password and register label
next_btn_font = ("Trebuchet MS", 17, "bold") # for the forget password and register label
phase_font = ("Trebuchet MS", 30, "bold") # for the login label
part1_font = ("Trebuchet MS", 20, "bold") # for the login label
part2_font = ("Trebuchet MS", 20, "bold") # for the login label
heading_font = ("Trebuchet MS", 17, "bold") # for the login label
subheading_font = ("Trebuchet MS", 17, "bold") # for the login label

root.config(bg=background)
root.resizable(False, False)
root.geometry("1250x700+210+100")

# show message box when closing the window
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        
root.protocol("WM_DELETE_WINDOW", on_closing) # call on_closing function when closing the window

# Register Frame
def open_register():
    global main_Frame, name_entry, email_entry, dob_entry, password_entry, number_entry, repassword_entry, show_password_var
    main_Frame.destroy()
    
    main_Frame = ctk.CTkFrame(root, width=724, height=587, corner_radius=30)
    main_Frame.grid(row=0, column=0, padx=278, pady=122)

    Sign_up_label = Label(main_Frame,
                          text="Sign Up",
                          font=font3,
                          bg=frame_clr,
                          fg=background)
    Sign_up_label.place(x=279, y=10)
    
    name_entry = ctk.CTkEntry(main_Frame,
                              width=291,
                              height=56,
                              font=font1,
                              placeholder_text="Name")
    name_entry.place(x=40, y=134)

    email_entry = ctk.CTkEntry(main_Frame,
                               width=291,
                               height=56,
                               font=font1,
                               placeholder_text="Email")
    email_entry.place(x=392, y=134)

    dob_entry = ctk.CTkEntry(main_Frame,
                             width=291,
                             height=56,
                             font=font1,
                             placeholder_text="Date of Birth")
    dob_entry.place(x=40, y=217)
    
    show_password_var = IntVar()
    password_entry = ctk.CTkEntry(main_Frame, width=291, height=56, font=font1, show="*", placeholder_text="Password")
    password_entry.place(x=392, y=217)
    
    show_password_cb = Checkbutton(main_Frame, variable=show_password_var,bg="#F9F9FB", command=toggle_pw_show)
    show_password_cb.place(x=640, y=233)

    number_entry = ctk.CTkEntry(main_Frame,
                                width=291,
                                height=56,
                                font=font1,
                                placeholder_text="Phone Number")
    number_entry.place(x=40, y=300)

    repassword_entry = ctk.CTkEntry(main_Frame,
                                    width=291,height=56,
                                    font=font1,
                                    show="*",
                                    placeholder_text="Re-enter Password")
    repassword_entry.place(x=392, y=300)

    singin_btn = ctk.CTkButton(main_Frame,
                               text="Sign Up",
                               width=134,
                               height=59,
                               font=font1,
                               command=validate_registration_form,
                               fg_color="#314C3B",
                               hover_color=background)

    singin_btn.place(x=292, y=387)

    already_have_account = ctk.CTkButton(main_Frame,
                                         text="Already have an account?",
                                         font=font2,
                                         text_color="black",
                                         fg_color=frame_clr,
                                         hover_color=frame_clr,
                                         command=threading2)

    already_have_account.place(x=258, y=486)
    
def toggle_pw_show():
    if show_password_var.get():
        password_entry.configure(show="")
        repassword_entry.configure(show="")
    else:
        password_entry.configure(show="*")
        repassword_entry.configure(show="*")

def validate_registration_form():
    name = name_entry.get()
    email = email_entry.get()
    dob = dob_entry.get()
    password = password_entry.get()
    repassword = repassword_entry.get()
    phone = number_entry.get()

    if not name or not email or not dob or not password or not repassword or not phone:
        messagebox.showerror("Registration Failed", "All fields are required!")
        return

    if not validate_email(email):
        messagebox.showerror("Registration Failed", "Invalid email format!")
        return

    if not validate_dob(dob):
        messagebox.showerror("Registration Failed", "Invalid date of birth format! Use YYYY-MM-DD.")
        return

    if password != repassword:
        messagebox.showerror("Registration Failed", "Passwords do not match!")
        return

    if not validate_phone(phone):
        messagebox.showerror("Registration Failed", "Invalid phone number!")
        return

    save_registration()  # Save the data to the database after successful validation

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def validate_dob(dob):
    dob_regex = r'^\d{4}-\d{2}-\d{2}$'
    return re.match(dob_regex, dob) is not None

def validate_phone(phone):
    return phone.isdigit() and len(phone) in (10, 13)
      
def save_registration():
    try:
        conn = db.connect("database.db")
        cursor = conn.cursor()

        # Get the email entered by the user
        email = email_entry.get()
        # receiver_email = email_entry.get()

        # Check if the email (username) already exists
        cursor.execute("SELECT * FROM user WHERE username = ?", (email,))
        if cursor.fetchone():
            messagebox.showerror("Registration Error", "Email already exists. Please use a different email.")
            return

        # Retrieve values from entry widgets
        name = name_entry.get()
        password = password_entry.get()
        dob = dob_entry.get()
        phone = number_entry.get()

        # Insert the new user into the database
        cursor.execute(
            "INSERT INTO user (username, password, name_1, dob_1, phone_1) VALUES (?, ?, ?, ?, ?)",
            (email, password, name, dob, phone),
        )
        conn.commit()

        # Send email to the registered user
        send_registration_email(email, name, password, phone, dob)

        messagebox.showinfo("Registration", "Registration Successful!")
    except db.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        conn.close()

    # Clear all entry fields after successful registration
    name_entry.delete(0, END)
    email_entry.delete(0, END)
    dob_entry.delete(0, END)
    password_entry.delete(0, END)
    number_entry.delete(0, END)
    repassword_entry.delete(0, END)

def send_registration_email(email, name, password, phone, dob):
    try:
        server = smtplib.SMTP_SSL("mail.sharmaanand.com.np", 465)  
        server.login("info@sharmaanand.com.np", "admin@444$")
        message = MIMEText(f"Dear {name},\n\nThank you for registering with us!\n\nHere are your registration details:\n\nName: {name}\nEmail:{email}\nPhone Number: {phone}\nDate of Birth: {dob}\nPassword: {password}\n\nBest regards,\nAnand Sharma", "plain")
        message["Subject"] = "Registration Confirmation"
        message["From"] = "info@sharmaanand.com.np"
        message["To"] = email

        server.sendmail(message["From"], message["To"], message.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

def logout():
    main_frame.destroy()
    logout_btn.destroy()
    t3 = Thread(target=create_login_frame)
    t3.start()

    
def open_phase2_part1():
    main_frame.destroy()
    t4 = Thread(target=phase2_part1)
    t4.start()
    main_Frame.destroy()
    
def open_phase2_part2():
    main_frame.destroy()
    t5 = Thread(target=phase2_part2)
    t5.start()
    main_Frame.destroy()
    
def medical_test():
    main_frame.destroy()
    t6 = Thread(target=phase3)
    t6.start()
    main_Frame.destroy()
    
def back_to_phase3():
    main_frame.destroy()
    t6 = Thread(target=phase3)
    t6.start()
    main_Frame.destroy()

def back_to_phase1():
    main_frame.destroy()
    t6 = Thread(target=open_phase1)
    t6.start()
    main_Frame.destroy()
    
def back_to_phase2_part1():
    main_frame.destroy()
    t6 = Thread(target=phase2_part1)
    t6.start()
    main_Frame.destroy()

def back_to_phase2_part2():
    main_frame.destroy()
    t6 = Thread(target=phase2_part2)
    t6.start()
    main_Frame.destroy()
    
# Phase 1    
def open_phase1():
    global main_frame, root, logout_btn
    
    # create a main frame
    main_frame = ctk.CTkFrame(root, width=1157, height=600, corner_radius=30, bg_color="transparent")
    main_frame.grid(row=0, column=1, padx=61, pady=150)
    
    # Entry Fields for Application Form
    # First Column
    first_name = ctk.CTkEntry(main_frame, width=486, height=56, font=font1, placeholder_text="First / middle Names", border_color=frame_clr)
    first_name.place(x=80, y=25)
    
    passport_no = ctk.CTkEntry(main_frame, width=486, height=56, font=font1, placeholder_text="Passport Number", border_color=frame_clr)
    passport_no.place(x=80, y=110)
    
    nnp_no = ctk.CTkEntry(main_frame, width=486, height=56, font=font1, placeholder_text="NNP Number",  border_color=frame_clr)
    nnp_no.place(x=80, y=195)
    
    father_name = ctk.CTkEntry(main_frame, width=486, height=56, font=font1, placeholder_text="Father's Name", border_color=frame_clr)
    father_name.place(x=80, y=280)
    
    mother_name = ctk.CTkEntry(main_frame, width=486, height=56, font=font1, placeholder_text="Mother's Name", border_color=frame_clr)
    mother_name.place(x=80, y=365)
    
    see_year = ctk.CTkEntry(main_frame, width=486, height=56, font=font1, placeholder_text="SEE Year", border_color=frame_clr)
    see_year.place(x=80, y=450)
    
    # Second Column
    
    surname = ctk.CTkEntry(main_frame, width=197, height=56, font=font1, placeholder_text="Surname", border_color=frame_clr)
    surname.place(x=640, y=25)
    
    main_thar = ctk.CTkEntry(main_frame, width=197, height=56, font=font1, placeholder_text="Main Thar", border_color=frame_clr)
    main_thar.place(x=640, y=110)
    
    attepmpt = ctk.CTkEntry(main_frame, width=197, height=56, font=font1, placeholder_text="Attempt", border_color=frame_clr)
    attepmpt.place(x=640, y=195)
    
    religion = ctk.CTkEntry(main_frame, width=197, height=56, font=font1, placeholder_text="Religion", border_color=frame_clr)
    religion.place(x=640, y=280)
    
    district = ctk.CTkEntry(main_frame, width=197, height=56, font=font1, placeholder_text="District", border_color=frame_clr)
    district.place(x=640, y=365)
    
    village = ctk.CTkEntry(main_frame, width=197, height=56, font=font1, placeholder_text="Village", border_color=frame_clr)
    village.place(x=640, y=450)
    
    # Third Column
    dob_ad = ctk.CTkEntry(main_frame, width=208, height=56, font=font1, placeholder_text="Date of Birth(AD)", border_color=frame_clr)
    dob_ad.place(x=900, y=25)
    
    dob_bd = ctk.CTkEntry(main_frame, width=208, height=56, font=font1, placeholder_text="Date of Birth(BD)", border_color=frame_clr)
    dob_bd.place(x=900, y=110)
    
    contact_no = ctk.CTkEntry(main_frame, width=208, height=56, font=font1, placeholder_text="Contact Number", border_color=frame_clr)
    contact_no.place(x=900, y=195)
    
    kin_contact = ctk.CTkEntry(main_frame, width=208, height=56, font=font1, placeholder_text="Kin's Contact Number", border_color=frame_clr)
    kin_contact.place(x=900, y=280)
    
    see_gpa = ctk.CTkEntry(main_frame, width=208, height=56, font=font1, placeholder_text="SEE GPA", border_color=frame_clr)
    see_gpa.place(x=900, y=365)
    
    blood_grp = ctk.CTkEntry(main_frame, width=208, height=56, font=font1, placeholder_text="Blood Group", border_color=frame_clr)
    blood_grp.place(x=900, y=450)
    
    # Log out button
    logout_btn = ctk.CTkButton(root, text="Log Out", width=100, height=40, font=font2, command=logout, fg_color="#314C3B", hover_color=background)
    logout_btn.place(x=1150, y=10)
    
    next_btn = ctk.CTkButton(main_frame, text="Next", width=120, height=40, corner_radius=10, font=font2, fg_color="#314C3B", bg_color=frame_clr,command=open_phase2_part1)
    next_btn.place(x=500, y=540)
    
# Phase 2 part one
def phase2_part1():
    global main_frame
    # create a main frame
    main_frame = ctk.CTkFrame(root, width=1157, height=520, corner_radius=30, bg_color="transparent")
    main_frame.grid(row=0, column=1, padx=61, pady=140)

    part1_lbl = Label(main_frame, text="Part 1".upper(), font=part1_font,bg=frame_clr)
    part1_lbl.place(x=20, y=5)

    heading_lbl = Label(main_frame, text="Applicant's Details - Must be Completed by the Applicant:".upper(), font=heading_font,bg=frame_clr)
    heading_lbl.place(x=235, y=50)

    # Entry Fields for Application Form
    # First Column
    full_name = ctk.CTkEntry(main_frame, width=1000, height=56, corner_radius=10,font=font1, placeholder_text="Name of Applicant (In Full)".upper(), border_color=frame_clr)
    full_name.place(x=80, y=110)

    address = ctk.CTkEntry(main_frame, width=650, height=56, corner_radius=10,font=font1, placeholder_text="Address of Applicant".upper(),  border_color=frame_clr)
    address.place(x=80, y=195)
    
    email = ctk.CTkEntry(main_frame, width=650, height=56, corner_radius=10,font=font1, placeholder_text="Email Address".upper(), border_color=frame_clr)
    email.place(x=80, y=280)

    citizenship = ctk.CTkEntry(main_frame, width=1000, height=56, corner_radius=10,font=font1, placeholder_text="NEPALESE CITIZENSHIP CERTIFICATE NO OF APPLICANT".upper(), border_color=frame_clr)
    citizenship.place(x=80, y=365)

    # Second Column
    date_of_birth = ctk.CTkEntry(main_frame, width=300, height=56, corner_radius=10,font=font1, placeholder_text="Date of Birth (AD)".upper(), border_color=frame_clr)
    date_of_birth.place(x=780, y=195)

    telephone_number = ctk.CTkEntry(main_frame, width=300, height=56, corner_radius=10,font=font1, placeholder_text="Telephone Number".upper(), border_color=frame_clr)
    telephone_number.place(x=780, y=280)

    next_btn = ctk.CTkButton(main_frame, text="Next", width=130, height=45, corner_radius=10, font=next_btn_font, fg_color="#314C3B", bg_color=frame_clr,command=open_phase2_part2)
    next_btn.place(x=980, y=455)
    
    back_btn = ctk.CTkButton(main_frame, text="back", width=130, height=45, corner_radius=10, font=next_btn_font, fg_color="#314C3B", bg_color=frame_clr,command=back_to_phase1)
    back_btn.place(x=30,y=445)

def phase2_part2():
    global main_frame
    # create a main frame
    main_frame = ctk.CTkFrame(root, width=1157, height=590, corner_radius=30, bg_color="transparent")
    main_frame.grid(row=0, column=1, padx=61, pady=120)

    part2_lbl = Label(main_frame, text="Part 2".upper(), font=font1,bg=frame_clr)
    part2_lbl.place(x=20, y=5)

    heading_lbl = Label(main_frame, text="EMERGENCY CONTACT DETAIL - MUST BE COMPLETED BY THE APPLICANT:".upper(), font=heading_font,bg=frame_clr)
    heading_lbl.place(x=235, y=20)

    # Entry Fields for Application Form
    # First Column
    part2_lbl = Label(main_frame, text="First Contact:".upper(), font=part2_font,bg=frame_clr)
    part2_lbl.place(x=80, y=75)

    fec_full_name = ctk.CTkEntry(main_frame, width=1000, height=56, font=font1,corner_radius=10, placeholder_text="Detail Full Name".upper(), border_color=frame_clr)
    fec_full_name.place(x=80, y=110)

    fec_address = ctk.CTkEntry(main_frame, width=720, height=56, font=font1, corner_radius=10,placeholder_text="Address".upper(),  border_color=frame_clr)
    fec_address.place(x=80, y=175)

    fec_mobile_number = ctk.CTkEntry(main_frame, width=550, height=56, font=font1, corner_radius=10,placeholder_text="Mobile Number".upper(), border_color=frame_clr)
    fec_mobile_number.place(x=80, y=240)

    part3_lbl = Label(main_frame, text="Second Contact:".upper(), font=subheading_font,bg=frame_clr)
    part3_lbl.place(x=80, y=300)

    sec_full_name = ctk.CTkEntry(main_frame, width=1000, height=56, font=font1, corner_radius=10,placeholder_text="Detail Full Name".upper(), border_color=frame_clr)
    sec_full_name.place(x=80, y=335)

    sec_address = ctk.CTkEntry(main_frame, width=720, height=56, font=font1,corner_radius=10, placeholder_text="Address".upper(),  border_color=frame_clr)
    sec_address.place(x=80, y=400)

    sec_mobile_number = ctk.CTkEntry(main_frame, width=550, height=56, font=font1, corner_radius=10,placeholder_text="Mobile Number".upper(), border_color=frame_clr)
    sec_mobile_number.place(x=80, y=465)

    # Second Column
    fec_date_of_birth = ctk.CTkEntry(main_frame, width=260, height=56, font=font1, corner_radius=10,placeholder_text="Date of Birth (AD)".upper(), border_color=frame_clr)
    fec_date_of_birth.place(x=820, y=175)

    fec_telephone_number = ctk.CTkEntry(main_frame, width=430, height=56, font=font1, corner_radius=10,placeholder_text="Telephone Number".upper(), border_color=frame_clr)
    fec_telephone_number.place(x=650, y=240)

    sec_date_of_birth = ctk.CTkEntry(main_frame, width=260, height=56, font=font1, corner_radius=10,placeholder_text="Date of Birth (AD)".upper(), border_color=frame_clr)
    sec_date_of_birth.place(x=820, y=400)

    sec_telephone_number = ctk.CTkEntry(main_frame, width=430, height=56, font=font1, corner_radius=10,placeholder_text="Telephone Number".upper(), border_color=frame_clr)
    sec_telephone_number.place(x=650, y=465)

    next_btn = ctk.CTkButton(main_frame, text="Next", width=130, height=45, corner_radius=10, font=next_btn_font, fg_color="#314C3B", bg_color=frame_clr,command=medical_test)
    next_btn.place(x=980, y=535)
    
    back_btn = ctk.CTkButton(main_frame, text="back", width=130, height=45, corner_radius=10, font=next_btn_font, fg_color="#314C3B", bg_color=frame_clr,command=back_to_phase2_part1)
    back_btn.place(x=30,y=535)
    
def show_medical_date():
    main_frame.destroy()
    t7 = Thread(target=medi_date_lbl)
    t7.start()
    main_Frame.destroy()

def show_physical_date():
    main_frame.destroy()
    t7 = Thread(target=Phy_ass_lbl)
    t7.start()
    main_Frame.destroy()

def show_education_date():
    main_frame.destroy()
    t7 = Thread(target=edu_ass_lbl)
    t7.start()
    main_Frame.destroy()
    
def show_int_date():
    main_frame.destroy()
    t7 = Thread(target=int_ass_lbl)
    t7.start()
    main_Frame.destroy()

def phase3():
    
    global main_frame, medical_btn, Physical_ass_btn, educational_ass_btn, intervie_btn
    # create a main frame
    main_frame = ctk.CTkFrame(root, width=941, height=575, corner_radius=30, bg_color="transparent")
    main_frame.grid(row=0, column=1, padx=170, pady=146)
    
    part3_lbl = Label(main_frame, text="Phase 3", font=phase_font, bg=frame_clr, fg='#6B7273')
    part3_lbl.place(x= 400, y= 20)
    
    medical_btn = ctk.CTkButton(main_frame, 
                                text="Medical",
                                width=691,
                                height=71,
                                corner_radius=10,
                                font=part1_font,
                                fg_color="#2D8A69",
                                text_color="white",
                                command=show_medical_date)
    medical_btn.place(x= 140, y= 97)
    Physical_ass_btn = ctk.CTkButton(main_frame, 
                                text="Physical Assessments",
                                width=691,
                                height=71,
                                corner_radius=10,
                                font=part1_font,
                                fg_color="#2D8A69",
                                text_color="white",
                                command=show_physical_date)
    Physical_ass_btn.place(x= 140, y= 199)
    educational_ass_btn = ctk.CTkButton(main_frame, 
                                text="Educational Assessments",
                                width=691,
                                height=71,
                                corner_radius=10,
                                font=part1_font,
                                fg_color="#2D8A69",
                                text_color="white",
                                command=show_education_date)
    educational_ass_btn.place(x= 140, y= 310)
    intervie_btn = ctk.CTkButton(main_frame, 
                                text="Interview",
                                width=691,
                                height=71,
                                corner_radius=10,
                                font=part1_font,
                                fg_color="#2D8A69",
                                text_color="white",
                                command=show_int_date)
    intervie_btn.place(x= 140, y= 403)
    
    back_btn = ctk.CTkButton(main_frame, text="back", width=130, height=45, corner_radius=10, font=next_btn_font, fg_color="#314C3B", bg_color=frame_clr,command=back_to_phase2_part2)
    back_btn.place(x=30,y=510)

    finish_btn = ctk.CTkButton(main_frame, text="Finish", width=130, height=45, corner_radius=10, font=next_btn_font, fg_color="#314C3B", bg_color=frame_clr,command=logout)
    finish_btn.place(x=700,y=510)
      
def medi_date_lbl():
    global main_frame
    # create a main frame
    main_frame = ctk.CTkFrame(root, width=941, height=282, corner_radius=30, bg_color="transparent")
    main_frame.grid(row=0, column=1, padx=170, pady=146)
    
    part3_lbl = Label(main_frame, text="Phase 3", font=phase_font, bg=frame_clr, fg='#6B7273')
    part3_lbl.place(x= 400, y= 20)
    
    medical_date_lbl = Label(main_frame, text="Medical Date: ", font=part1_font, bg=frame_clr, fg='black', width=20, height=2)
    medical_date_lbl.place(x= 190, y= 100)
    
    display_date_lbl = Label(main_frame, text="Year-Month-Day", font=part1_font, bg='white', fg='black', width=20, height=2)
    display_date_lbl.place(x= 380, y= 100)
    
    back_btn = ctk.CTkButton(main_frame, text="back", width=130, height=45, corner_radius=10, font=next_btn_font, fg_color="#314C3B", bg_color=frame_clr,command=back_to_phase3)
    back_btn.place(x=30,y=220)

def Phy_ass_lbl():
    global main_frame
    # create a main frame
    main_frame = ctk.CTkFrame(root, width=941, height=282, corner_radius=30, bg_color="transparent")
    main_frame.grid(row=0, column=1, padx=170, pady=146)
    
    part3_lbl = Label(main_frame, text="Phase 3", font=phase_font, bg=frame_clr, fg='#6B7273')
    part3_lbl.place(x= 400, y= 20)
    
    Physical_ass_lbl_lbl = Label(main_frame, text="Physical Assessments", font=part1_font, bg=frame_clr, fg='black', width=20, height=2)
    Physical_ass_lbl_lbl.place(x= 150, y= 100)
    
    display_date_lbl = Label(main_frame, text="Year-Month-Day", font=part1_font, bg='white', fg='black', width=20, height=2)
    display_date_lbl.place(x= 390, y= 100)
    
    back_btn = ctk.CTkButton(main_frame, text="back", width=130, height=45, corner_radius=10, font=next_btn_font, fg_color="#314C3B", bg_color=frame_clr,command=back_to_phase3)
    back_btn.place(x=30,y=220)

def edu_ass_lbl():
    global main_frame
    # create a main frame
    main_frame = ctk.CTkFrame(root, width=941, height=282, corner_radius=30, bg_color="transparent")
    main_frame.grid(row=0, column=1, padx=170, pady=146)
    
    part3_lbl = Label(main_frame, text="Phase 3", font=phase_font, bg=frame_clr, fg='#6B7273')
    part3_lbl.place(x= 400, y= 20)
    
    Physical_ass_lbl_lbl = Label(main_frame, text="Educational Assessments", font=part1_font, bg=frame_clr, fg='black', width=20, height=2)
    Physical_ass_lbl_lbl.place(x= 150, y= 100)
    
    display_date_lbl = Label(main_frame, text="Year-Month-Day", font=part1_font, bg='white', fg='black', width=20, height=2)
    display_date_lbl.place(x= 390, y= 100)

    back_btn = ctk.CTkButton(main_frame, text="back", width=130, height=45, corner_radius=10, font=next_btn_font, fg_color="#314C3B", bg_color=frame_clr,command=back_to_phase3)
    back_btn.place(x=30,y=220)

    
def int_ass_lbl():

    global main_frame
    # create a main frame
    main_frame = ctk.CTkFrame(root, width=941, height=282, corner_radius=30, bg_color="transparent")
    main_frame.grid(row=0, column=1, padx=170, pady=146)
    
    part3_lbl = Label(main_frame, text="Phase 3", font=phase_font, bg=frame_clr, fg='#6B7273')
    part3_lbl.place(x= 400, y= 20)
    
    Physical_ass_lbl_lbl = Label(main_frame, text="Interview", font=part1_font, bg=frame_clr, fg='black', width=20, height=2)
    Physical_ass_lbl_lbl.place(x= 150, y= 100)
    
    display_date_lbl = Label(main_frame, text="Year-Month-Day", font=part1_font, bg='white', fg='black', width=20, height=2)
    display_date_lbl.place(x= 390, y= 100)

    back_btn = ctk.CTkButton(main_frame, text="back", width=130, height=45, corner_radius=10, font=next_btn_font, fg_color="#314C3B", bg_color=frame_clr,command=back_to_phase3)
    back_btn.place(x=30,y=220)

# Save Login Information
def save_login():
    global username, password
    uname = username.get()
    pwd = password.get()

    if not uname or not pwd:
        messagebox.showerror("Login Failed", "Username and Password cannot be empty!")
        return

    try:
        conn = db.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user WHERE username = ? AND password = ?", (uname, pwd))
        row = cursor.fetchone()
        if row:
            messagebox.showinfo("Login Success", "Login Successful!")
            open_phase1()
        else:
            messagebox.showerror("Login Failed", "Invalid Username or Password!")
    except db.Error as e:
        messagebox.showerror("Database Error", str(e))
    finally:
        conn.close()

# Login Frame
def create_login_frame():

    global main_Frame, username, password
    main_Frame = ctk.CTkFrame(master=root, width=555, height=431, corner_radius=30)
    main_Frame.grid(row=0, column=1, padx=350, pady=150)

    login_label = Label(main_Frame, text="Login", font=font3, bg=frame_clr, fg=background)
    login_label.place(x=200, y=18)

    username = ctk.CTkEntry(main_Frame, width=487, height=56, corner_radius=10, font=font1,
                            fg_color=background, text_color=framefg, placeholder_text="Username",
                            placeholder_text_color=framefg)
    username.place(x=40, y=130)

    password = ctk.CTkEntry(main_Frame, width=487, height=56, corner_radius=10, font=font1, show="*",
                            fg_color=background, text_color=framefg, placeholder_text="Password",
                            placeholder_text_color=framefg)
    password.place(x=40, y=210)

    login_Btn = ctk.CTkButton(main_Frame, text="Login", width=120, height=40, corner_radius=10, font=font2,
                              command=save_login, fg_color="#314C3B")
    login_Btn.place(x=200, y=290)

    forgot_Btn = ctk.CTkButton(main_Frame, text="Forgot Password?", font=font2, text_color=background,
                               fg_color=frame_clr, command=lambda: print("Forgot Password"),
                               hover_color=frame_clr)
    forgot_Btn.place(x=40, y=360)

    new_Account_Btn = ctk.CTkButton(main_Frame, text="Don't have Account?", font=font2, text_color=background,
                                    fg_color=frame_clr, command=threading, hover_color=frame_clr)
    new_Account_Btn.place(x=350, y=360)

    try:
        imageOne = ImageTk.PhotoImage(Image.open("Assets/logo.png").resize((150, 115)))
        logo_icon = Label(root, image=imageOne, bg=background)
        logo_icon.image = imageOne
        logo_icon.place(x=20, y=0)

        imageThree = ImageTk.PhotoImage(Image.open("Assets/user.png").resize((31, 31)))
        User_icon = Label(main_Frame, image=imageThree, bg=background)
        User_icon.image = imageThree
        User_icon.place(x=470, y=139)

        imageTwo = ImageTk.PhotoImage(Image.open("Assets/password.png").resize((31, 31)))
        password_icon = Label(main_Frame, image=imageTwo, bg=background)
        password_icon.image = imageTwo
        password_icon.place(x=470, y=218)
    except Exception as e:
        messagebox.showerror("Image Error", str(e))

initialize_database()
create_login_frame() # create login frame

root.mainloop()