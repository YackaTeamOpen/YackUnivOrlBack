from .. import db


# CREATE TABLE `yackadb`.`community_code` ( `id` INT NOT NULL AUTO_INCREMENT , `code` TEXT NOT NULL , PRIMARY KEY (`id`)) ENGINE = InnoDB;
class Community_code(db.Model):
    """Model for a community code"""

    __tablename__ = "community_code"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(500), unique=True, nullable=False)

    def __repr__(self):
        return "<Community_code {} {}>".format(
            self.id,
            self.code,
        )
