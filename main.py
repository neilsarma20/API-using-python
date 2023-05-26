from flask import *
import json, time

app = Flask(__name__)

# In-memory storage for events (replace with a database in production)
events = []

# GET /events?id=:event_id
@app.route('/api/v3/app/events', methods=['GET'])
def get_event_by_id():
    event_id = request.args.get('id')
    for event in events:
        if event['uid'] == event_id:
            return jsonify(event)
    return jsonify({'error': 'Event not found'})

# GET /events?type=latest&limit=5&page=1
@app.route('/api/v3/app/events', methods=['GET'])
def get_latest_events():
    event_type = request.args.get('type')
    limit = int(request.args.get('limit', 5))
    page = int(request.args.get('page', 1))
    # Pagination logic goes here
    # You can return a subset of events based on the provided parameters
    return jsonify(events[:limit])

# POST /events
@app.route('/api/v3/app/events', methods=['POST'])
def create_event():
    payload = request.form
    event = {
        'uid': len(events) + 1,
        'type': 'event',
        'name': payload['name'],
        'tagline': payload['tagline'],
        'schedule': payload['schedule'],
        'description': payload['description'],
        'moderator': payload['moderator'],
        'category': payload['category'],
        'sub_category': payload['sub_category'],
        'rigor_rank': int(payload['rigor_rank']),
        'attendees': []
    }
    events.append(event)
    return jsonify({'event_id': event['uid']})

# PUT /events/:id
@app.route('/api/v3/app/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    for event in events:
        if event['uid'] == event_id:
            payload = request.form
            event.update({
                'name': payload.get('name', event['name']),
                'tagline': payload.get('tagline', event['tagline']),
                'schedule': payload.get('schedule', event['schedule']),
                'description': payload.get('description', event['description']),
                'moderator': payload.get('moderator', event['moderator']),
                'category': payload.get('category', event['category']),
                'sub_category': payload.get('sub_category', event['sub_category']),
                'rigor_rank': int(payload.get('rigor_rank', event['rigor_rank']))
            })
            return jsonify({'message': 'Event updated successfully'})
    return jsonify({'error': 'Event not found'})

# DELETE /events/:id
@app.route('/api/v3/app/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    for event in events:
        if event['uid'] == event_id:
            events.remove(event)
            return jsonify({'message': 'Event deleted successfully'})
    return jsonify({'error': 'Event not found'})

if __name__ == '__main__':
    app.run()
