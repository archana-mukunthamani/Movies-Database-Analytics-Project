
USE Movies_db;
GO
-- Top Rated Movies By Subscription Status 

WITH TopMovies AS (
    SELECT TOP 10
        m.MovieID,
        m.Title,
        ROUND(AVG(r.Rating), 2) AS Overall_Average_Rating,
        COUNT(r.RatingID) AS Total_Ratings
    FROM Ratings r
    JOIN Movies m
        ON r.MovieID = m.MovieID
    GROUP BY m.MovieID, m.Title
    HAVING COUNT(r.RatingID) >= 5
    ORDER BY Overall_Average_Rating DESC
)
SELECT
    tm.Title,
    tm.Overall_Average_Rating,
    u.SubscriptionStatus,
    ROUND(AVG(r.Rating), 2) AS Average_Rating,
    COUNT(r.RatingID) AS Number_of_Ratings
FROM TopMovies tm
JOIN Ratings r
    ON tm.MovieID = r.MovieID
JOIN Users u
    ON r.UserID = u.UserID
GROUP BY
    tm.Title,
    tm.Overall_Average_Rating,
    u.SubscriptionStatus
ORDER BY
    tm.Overall_Average_Rating DESC,
    u.SubscriptionStatus;

-- Most Popular Genres by Total views and subscription status 

WITH GenreViews AS (
    SELECT
        u.SubscriptionStatus,
        TRIM(value) AS Genre,
        SUM(m.Total_Views) AS Total_Views
    FROM Users u
    JOIN Ratings r
        ON u.UserID = r.UserID
    JOIN Movies m
        ON r.MovieID = m.MovieID
    CROSS APPLY STRING_SPLIT(m.Genres, '|')
    GROUP BY
        u.SubscriptionStatus,
        TRIM(value)
),
TopGenres AS (
    SELECT TOP 10
        Genre,
        SUM(Total_Views) AS Overall_Total_Views
    FROM GenreViews
    GROUP BY Genre
    ORDER BY Overall_Total_Views DESC
)
SELECT
    gv.Genre,
    gv.SubscriptionStatus,
    gv.Total_Views
FROM GenreViews gv
JOIN TopGenres tg
    ON gv.Genre = tg.Genre
ORDER BY
    tg.Overall_Total_Views DESC,
    gv.SubscriptionStatus;


-- User Distribution by Age group and subscription status 


SELECT
    SubscriptionStatus,
    CASE
        WHEN Age < 18 THEN 'Under 18'
        WHEN Age BETWEEN 18 AND 24 THEN '18-24'
        WHEN Age BETWEEN 25 AND 34 THEN '25-34'
        WHEN Age BETWEEN 35 AND 44 THEN '35-44'
        WHEN Age BETWEEN 45 AND 54 THEN '45-54'
        ELSE '55+'
    END AS Age_Group,
    COUNT(UserID) AS User_Count
FROM Users
GROUP BY
    SubscriptionStatus,
    CASE
        WHEN Age < 18 THEN 'Under 18'
        WHEN Age BETWEEN 18 AND 24 THEN '18-24'
        WHEN Age BETWEEN 25 AND 34 THEN '25-34'
        WHEN Age BETWEEN 35 AND 44 THEN '35-44'
        WHEN Age BETWEEN 45 AND 54 THEN '45-54'
        ELSE '55+'
    END
ORDER BY
    SubscriptionStatus,
    Age_Group;

-- user Distribution by subscription status 


SELECT
    SubscriptionStatus,
    COUNT(*) AS User_Count
FROM Users
GROUP BY SubscriptionStatus;


-- User distribution by country and subscription status 

SELECT
    Country,
    SubscriptionStatus,
    COUNT(UserID) AS User_Count
FROM Users
GROUP BY
    Country,
    SubscriptionStatus
ORDER BY
    Country,
    SubscriptionStatus;

-- Device usage distribution by subscription status 


SELECT
    Device,
    SubscriptionStatus,
    COUNT(UserID) AS User_Count
FROM Users
GROUP BY
    Device,
    SubscriptionStatus
ORDER BY
    Device,
    SubscriptionStatus;
