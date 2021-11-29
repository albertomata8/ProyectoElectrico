import smtplib 
# from decouple import config
import os


# class email_server:
def send_book_table(usuario, cantidad_personas, fecha, hora, email):    
    # message = 'Se le confirma su reservacion para' + str(cantidad_personas) + ', el día ' + str(fecha) + ', a la hora ' + str(hora)
    message = 'Se le confirma su mesa para ' + str(cantidad_personas) + ', en la fecha ' + str(fecha) + ', a la hora ' + str(hora)
    subject = 'Confirmacion de reserva del restaurante Basho, estimado: ' + str(usuario)

    message = 'Subject: {}\n\n{}'.format(subject,message)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    server.login('bashosushicr@gmail.com', 'Ibiza1620')

    server.sendmail('bashosushicr@gmail.com',email, message)

    server.quit()


def conf_email(usuario, email):
    message = 'Gracias por registrarse en nuestra pagina Basho. \n\n Estamos para servirle.'
    subject = 'Confirmacion de cuenta ' + str(usuario)

    message = 'Subject: {}\n\n{}'.format(subject,message)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    server.login('bashosushicr@gmail.com', 'Ibiza1620')

    server.sendmail('bashosushicr@gmail.com',email, message)

    server.quit()

def cancel_book_table(usuario, cantidad_personas, fecha, hora, email):    
    # message = 'Se le confirma su reservacion para' + str(cantidad_personas) + ', el día ' + str(fecha) + ', a la hora ' + str(hora)
    message = 'Se le confirma la cancelacion su mesa para ' + str(cantidad_personas) + ', en la fecha ' + str(fecha) + ', a la hora ' + str(hora)
    subject = 'Cancelacion de reserva del restaurante Basho, estimado: ' + str(usuario)

    message = 'Subject: {}\n\n{}'.format(subject,message)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    server.login('bashosushicr@gmail.com', 'Ibiza1620')

    server.sendmail('bashosushicr@gmail.com',email, message)

    server.quit()
