from services.emailServices import EmailServices
class emailControllers:
    @staticmethod
    def send_email(request):
        try:
        # send email
            data = request.get_json()
            email = data['email']
            subject = data['subject']
            message = data['message']
            EmailServices.sendEmail(email, subject, message)
            return {'message': 'Email sent successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 400