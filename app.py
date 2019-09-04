import google

from flask import Flask, render_template, url_for, request, redirect
import json
import os
import html

from werkzeug.wrappers import response

from api import get_transcript
from db import get_base_info, get_segment, db
from google_diff_patch_match.diff_match_patch import diff_match_patch
from preparation import download_file, split_file, OUTPUT_DIR


app = Flask(__name__)


# Just want to slightly change the output of the Google differ.
class Differ(diff_match_patch):

    def diff_prettyHtml(self, diffs):
        """Convert a diff array into a pretty HTML report.

        Args:
          diffs: Array of diff tuples.

        Returns:
          HTML representation.
        """

        html_google = []
        for (op, data) in diffs:
            text = html.escape(data)
            if op == self.DIFF_INSERT:
                html_google.append("<ins style=\"background:#e6ffe6;\">{}</ins>".format(text))
            elif op == self.DIFF_DELETE:
                html_google.append("<del style=\"background:#ffe6e6;\">{}</del>".format(text))
            elif op == self.DIFF_EQUAL:
                html_google.append("<span>{}</span>".format(text))
        return '<div id="google_solution">{}</div>'.format("".join(html_google))


# Utility functions
def _get_segment(obj, file_id, position, update=False):
    full_filename = _get_full_filename(obj, position)
    segment = get_segment(file_id, position)

    if segment.transcript is None and update:
        get_transcript(full_filename)

    return segment


def _get_full_filename(obj, position):
    dirname = '{}/{}'.format('mp3', obj.id)
    # TODO: Hardcoded length
    filename = obj.filename.replace('.mp3', '.{:04}'.format(int(position)))
    return '{}/{}.mp3'.format(dirname, '30_{}'.format(filename))


@app.route('/_retrieve/<file_id>/<position>', methods=['POST'])
def retrieve_transcript(file_id, position):
    try:
        obj = get_base_info(file_id)
        _get_segment(obj, file_id, position, update=True)
        return render_template('get_transcript', position=position)
    except (google.api_core.exceptions.GoogleAPICallError, google.api_core.exceptions.RetryError,
            google.auth.exceptions.DefaultCredentialsError) as e:
        print('HANDLING THE ERROR')
        return render_template('get_transcript.html', error=e)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        pretty_name = request.form.get('pretty_name')
        if not url:
            return 'You did not specify a URL!', 400
        # file_id, download_path = download_file(url, pretty_name=pretty_name)
        file_id, download_path = 3, './static/mp3/3/5566149.mp3'
        split_file(file_id, download_path)
        return redirect(url_for('play_file', file_id=file_id, position=1, code=301))

    return render_template('base.html')


@app.route('/file/<file_id>/<position>')
def play_file(file_id, position=1):
    obj = get_base_info(file_id)
    full_filename = _get_full_filename(obj, position)
    segment = _get_segment(obj, file_id, position, update=False)

    return render_template('main.html', files=sorted(obj.segments, reverse=False), filename=full_filename,
                           file_id=file_id, position=position, segment=segment)


@app.route('/file/<file_id>/<position>/solution', methods=['GET', 'POST'])
def solution(file_id, position):
    obj = get_base_info(file_id)
    full_filename = _get_full_filename(obj, position)
    segment = get_segment(obj, file_id, position)
    confidence = '0' if not segment.confidence else '{:.2f}'.format(segment.confidence)

    if request.method == 'GET':

        return render_template('view_solution.html', files=sorted(obj.segments, reverse=False), file_id=file_id,
                               filename=full_filename, google_solution=segment.transcript,
                               confidence=confidence, position=position)
    else:
        # if segment.transcript is None:
        #     transcript, confidence = get_transcript(full_filename)
        #     segment.transcript = transcript
        #     segment.confidence = confidence
        #
        # db.commit()
        student_solution = request.form.get('student_answer')

        differ = Differ()

        google_solution = differ.diff_prettyHtml(differ.diff_main(student_solution, segment.transcript))
        return render_template('solution.html', files=sorted(obj.segments, reverse=False), file_id=file_id,
                               filename=full_filename, student_solution=student_solution, google_solution=google_solution,
                               confidence='{:.2f}'.format(segment.confidence))


if __name__ == '__main__':
    app.run(host='0.0.0.0')
