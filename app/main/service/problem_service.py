from main.model.problem import Problem


def getAllProblem():
    return Problem.query.all()


def getProblemById(problem_id):
    return Problem.query.filter_by(id=problem_id).first()
