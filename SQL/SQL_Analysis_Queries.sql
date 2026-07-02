--1. Top 10 Movies by Average Ratings
USE Movies_db;
GO

SELECT TOP 10
    m.Title,
    ROUND(AVG(r.Rating), 2) AS Average_Rating,
    COUNT(r.RatingID) AS Number_of_Ratings
FROM Ratings r
JOIN Movies m
    ON r.MovieID = m.MovieID
GROUP BY m.Title
--HAVING COUNT(r.RatingID) >= 5
ORDER BY Average_Rating DESC;


--2. Most Popular Genres - Measures popularity by the number of movies in each genre.
--Interpretation: Which genres have the most titles available?

SELECT TOP 10
    Genres,
    COUNT(MovieID) AS Number_of_Movies
FROM Movies
GROUP BY Genres
ORDER BY Number_of_Movies DESC;



-- Most Popular Genres by Total Views
--Interpretation: Which genres attract the most viewing activity?

SELECT
    Genres,
    SUM(Total_Views) AS Total_Views
FROM Movies
GROUP BY Genres
ORDER BY Total_Views DESC;

--Highest Rated Genres
-- Interpretation: Which genres are most highly rated by users?

SELECT
    m.Genres,
    ROUND(AVG(r.Rating),2) AS Average_Rating,
    COUNT(r.RatingID) AS Number_of_Ratings
FROM Ratings r
JOIN Movies m
    ON r.MovieID = m.MovieID
GROUP BY m.Genres
HAVING COUNT(r.RatingID) >= 5
ORDER BY Average_Rating DESC;



-- Measures popularity by engagement.
--Interpretation: Which genres receive the most user ratings?
SELECT
    m.Genres,
    COUNT(r.RatingID) AS Number_of_Ratings
FROM Ratings r
JOIN Movies m
    ON r.MovieID = m.MovieID
GROUP BY m.Genres
ORDER BY Number_of_Ratings DESC;



--3. User Distribution by Age Group 

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


-- 4. Distribution of Users by Subscription Status

SELECT
    SubscriptionStatus,
    COUNT(*) AS User_Count
FROM Users
GROUP BY SubscriptionStatus;

-- 5. User Distribution by Country

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

-- 6. Distribution of Device Usage Among Users


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


