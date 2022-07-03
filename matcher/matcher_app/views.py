from html import entities
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .database import cursor

# Number of columns in candidates table
ID_COL = 0
NAME_COL = 1
TITLE_COL = 2
SKILLS_COL = 3 

@csrf_exempt
def matching(request):
    body = json.loads(request.body)
    sql = create_query(body['title'], body['skills'])
    cursor.execute(sql)
    result_db = cursor.fetchall()
    all_rated_candidates = sort_candidate_by_rating(result_db, body['skills'])
    if 'page' in body.keys():
        page = body['page']
        top_rated = all_rated_candidates[(page - 1) * 20 : (page * 20)]
    else:
        top_rated = all_rated_candidates[0 : 20]
    jsonString = json.dumps(top_rated, indent=1)
    return HttpResponse(jsonString)

def create_query(title, skills):
    title_low = title.lower()
    query = "SELECT * FROM candidates WHERE"
    query += f" title LIKE '%{title_low}%'"
    if 'engineer' in title_low:
        first_word = title_low.split(' ')[0]
        query += f" OR title LIKE '%{first_word} developer%'"
    if 'developer' in title_low:
        first_word = title_low.split(' ')[0]
        query += f" OR title LIKE '%{first_word} engineer%'"
    query += ' AND ('
    for idx, skill in enumerate(skills):
        if idx != len(skills) - 1:
            query += f" skills LIKE '%{skill.lower()}%' OR"
        else:
            query += f" skills LIKE '%{skill.lower()}%')"
    return query

def sort_candidate_by_rating(candidates_db, skills):
    candidates = []
    for candidate in candidates_db:
        candidate_rating = rate_candidate(candidate[SKILLS_COL], skills)
        candidate = {
            'name': candidate[1],
            'title': candidate[2],
            'skills': candidate[3].split(', '),
            'rating': candidate_rating
        }
        candidates.append(candidate)
    candidates.sort(key= lambda x: x['rating'], reverse=True)
    return candidates

def rate_candidate(personal_skills, needed_skills):
    num_needed_skills = len(needed_skills)
    num_matching_skills = 0
    personal_skills = personal_skills.split(', ')
    for needed_skill in needed_skills:
        if needed_skill.lower() in personal_skills:
            num_matching_skills += 1
    match_precentages = round((num_matching_skills/num_needed_skills)*100)
    return match_precentages