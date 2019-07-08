"""Controller code module"""

from flask import Request
from flask_restful import Resource, marshal_with
from injector import inject

from model import NOTE_FIELDS
from service import UserService, NoteService

DEFAULT_PAGE_SIZE = 20

class NotesList(Resource):
    """Notes Resource: The API for notes requests"""
    @inject
    def __init__(self, user_request: Request, user_service: UserService,
                 note_service: NoteService):
        self._request = user_request
        self._user_service = user_service
        self._note_service = note_service

    @marshal_with(NOTE_FIELDS)
    def get(self, uid):
        """GET HTTP method manager"""
        if not self._user_service.check_user_exists(uid):
            return None

        page = int(self._request.args.get('page', 0))
        page_size = int(self._request.args.get('page_size', DEFAULT_PAGE_SIZE))

        return self._note_service.find_all(page, page_size, uid=uid)

    @marshal_with(NOTE_FIELDS)
    def post(self, uid):
        """POST HTTP method manager: Creates new notes"""
        if not self._user_service.check_user_exists(uid):
            return None

        note_data = self._request.get_json(force=True)

        # TODO: handle validation errors
        if note_data is not None:
            note_data['uid'] = uid
            new_note = self._note_service.create_new(**note_data)
            new_note.save()
            new_note.reload()

            return new_note

        # FIXME: throw an HTTP error
        return None
