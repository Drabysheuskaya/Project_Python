CREATE TABLE File (
    FileId   integer     NOT NULL PRIMARY KEY,
    Filename varchar(50) NOT NULL
);

CREATE TABLE Location (
    LocationId integer NOT NULL PRIMARY KEY,
    X          integer NOT NULL,
    Y          integer NOT NULL,
    File       integer NOT NULL,
    CONSTRAINT Location_File FOREIGN KEY (File) REFERENCES File (FileId)
);

CREATE TABLE Room ( 
    RoomId   integer     NOT NULL PRIMARY KEY AUTOINCREMENT,
    RoomName varchar(20) NOT NULL,
    Location integer     NOT NULL,
    CONSTRAINT Room_Location FOREIGN KEY (Location) REFERENCES Location (LocationId)
);

CREATE TABLE Student ( 
    Number   integer     NOT NULL PRIMARY KEY,
    Password varchar(50) NOT NULL,
    Name     varchar(50) NOT NULL, 
    Surname  varchar(50) NOT NULL
);

CREATE TABLE Subject (
    SubjectId integer     NOT NULL PRIMARY KEY AUTOINCREMENT,
    Name      varchar(10) NOT NULL
);

CREATE TABLE Schedule (
    ScheduleId integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    Start      integer NOT NULL,
    End        integer NOT NULL,
    Student    integer NOT NULL,
    Subject    integer NOT NULL,
    Room       integer NOT NULL,
    CONSTRAINT Schedule_Room    FOREIGN KEY (Room)    REFERENCES Room (RoomId),
    CONSTRAINT Schedule_Student FOREIGN KEY (Student) REFERENCES Student (Number),
    CONSTRAINT Schedule_Subject FOREIGN KEY (Subject) REFERENCES Subject (SubjectId)
);
