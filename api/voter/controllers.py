from apiflask import APIBlueprint

voters = APIBlueprint("voter", __name__, tag="Voter", url_prefix="/api/v1/voters")

############################################
##                 VOTER                  ##
############################################
@voters.post("/signup")
@voters.doc(summary="Voter Signup", description="An endpoint for voter signup")
def voter_signup(data):
    pass


@voters.post("/signup-bulk")
@voters.doc()
def voter_bulk_signup():
    pass


@voters.post("/login")
@voters.doc(summary="Voter Login", description="An endpoint for voter login")
def voter_login(data):
    pass


@voters.get("/<id>")
@voters.doc()
def voter_get_by_id():
    pass


@voters.get("")
@voters.doc()
def voter_get_all():
    pass


@voters.get("/<id>/mini-elections")
@voters.doc(
    summary="Voter Mini Elections",
    description="An endpoint to get all mini elections for voter",
)
def voter_get_mini_elections(id, data):
    pass


@voters.post("/")
@voters.doc(
    summary="Voter Cast Vote",
    description="An endpoint for the voter to cast his vote in a mini election",
)
def voter_cast_vote():
    pass


@voters.post("/logout")
@voters.doc(summary="Voter Logout", description="An endpoint for the voter to logout")
def voter_logout():
    pass


############################################
##                 VOTER GROUP            ##
############################################
@voters.post("/groups")
@voters.doc(
    summary="Create Voter Group",
    description="An endpoint for the administrator to create a voter group",
)
def voter_group_create():
    pass


@voters.get("/groups")
@voters.doc(
    summary="Get Voter Group By Id",
    description="An endpoint to get the voter group by ID",
)
def voter_group_get_by_id():
    pass


@voters.get("/groups/all")
@voters.doc(
    summary="Get All Voter Groups", description="An endpoint to get all voter groups "
)
def voter_group_get_all():
    pass


@voters.delete("/groups")
@voters.doc(
    summary="Delete Voter Group",
    description="An endpoint for the administrator to delete a voter group",
)
def voter_group_delete():
    pass


@voters.put("/groups")
@voters.doc(
    summary="Modify Voter Group",
    description="An endpoint for the administrator to modify a voter group",
)
def voter_group_modify():
    pass
