from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from credentials import get_credentials

class GmailReader(object):
    def __init__(self, creds=None):
        if creds is None:
            creds = get_credentials()
        self.service = build('gmail', 'v1', credentials=creds)
        self.label_lookup = {}
    def get_id(self, label):
        all_labels = self.service.users().labels().list(userId='me').execute()
        matching_id = [d['id'] for d in all_labels['labels'] if d['name'] == label][0]
        self.label_lookup[label] = matching_id
    def get_mail_with_label(self, label):
        if not label in self.label_lookup.keys():
            self.get_id(label)
        matching_id = self.label_lookup[label]
        matches = self.service.users().messages().list(userId='me',labelIds=[matching_id]).execute()
        return matches
    def check_interactive_jobs(self):
        try:
            interactive_ready = self.get_mail_with_label('automation/interactive ready')
            interactive_completed = self.get_mail_with_label('automation/interactive completed')
            if interactive_ready['resultSizeEstimate'] > interactive_completed['resultSizeEstimate']:
                return 'Interactive job is ready!!!!'
            else:
                return 'No interactive jobs active.'
        except HttpError as error:
            print(f'An error occurred: {error}')
            return 'Could not check job status.'
    def check_batch_jobs(self):
        try:
            jobs_completed = self.get_mail_with_label('automation/job completed')
            if jobs_completed['resultSizeEstimate'] > 0:
                msg_ids = [d['id'] for d in jobs_completed['messages']]
                last_msg = self.service.users().messages().get(id=msg_ids[-1], userId='me').execute()
                if 'COMPLETED' in last_msg['snippet']:
                    return 'Slurm job completed.'
                elif 'EXITED' in last_msg['snippet']:
                    return 'Slurm job exited.'
                else:
                    return 'Unrecognized job completion status.'
            else:
                return 'No jobs to report.'
        except HttpError as error:
            print(f'An error occurred: {error}')
            return 'Could not check job status.'

if __name__ == '__main__':
    reader = GmailReader()
    print(reader.check_interactive_jobs())
    print(reader.check_batch_jobs())
