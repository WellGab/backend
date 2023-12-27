db.createUser(
    {
        user: "mongodb",
        pwd: "",
        roles: [
            {
                role: "readWrite",
                db: "wellgab"
            }
        ]
    }
);