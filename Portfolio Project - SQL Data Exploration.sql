/* user=vlam reportName=Portfolio Project - SQL Data Exploration reportSummary: Multiple queries written to display the different techniques used for SQL data exploration for my portfolio project */ 
----------------------------------------------------------------------------------------------------
--	Select and view everything from the COVID Deaths table
SELECT *
FROM [Portfolio Project].dbo.Covid_Deaths
ORDER BY 3, 4


----------------------------------------------------------------------------------------------------
--	Select and view everything from the COVID Vaccinations table
/*
SELECT *
FROM [Portfolio Project]..Covid_Vaccinations
ORDER BY 3, 4
*/


----------------------------------------------------------------------------------------------------
--	Select specific columns that we want to view from the table
SELECT 
	location,
	date,
	total_cases,
	new_cases,
	total_deaths,
	population
FROM 
	[Portfolio Project]..Covid_Deaths
ORDER BY 
	1, 2


----------------------------------------------------------------------------------------------------
--	Total Cases vs Total Deaths	
--	Shows the likelihood of dying if you contract COVID-19 in your country
SELECT 
	location, date, total_cases, total_deaths, (total_deaths/total_cases) * 100 as Death_Percentage
FROM 
	[Portfolio Project]..Covid_Deaths
WHERE 
	location LIKE '%states%'
ORDER BY 
	1, 2


----------------------------------------------------------------------------------------------------
--	Total Cases vs Population
--	Shows the percentage of population contracted COVID-19
SELECT location, date, population, total_cases, (total_cases/population) * 100 as Population_Infected_Percentage
FROM [Portfolio Project]..Covid_Deaths
WHERE location LIKE '%states%'
ORDER BY 1, 2


----------------------------------------------------------------------------------------------------
--	Countries with highest infection rate compared to population
SELECT location, population, MAX(total_cases) as Highest_Infection_Count , MAX( (total_cases/population) ) * 100 as Population_Infected_Percentage
FROM [Portfolio Project]..Covid_Deaths
GROUP BY location, population
ORDER BY Population_Infected_Percentage DESC


----------------------------------------------------------------------------------------------------
-- Countries with highest death rate per population
SELECT location,  MAX( CAST( total_deaths AS int ) ) as Total_Death_Count
FROM [Portfolio Project]..Covid_Deaths
WHERE continent IS NOT NULL
GROUP BY location
ORDER BY Total_Death_Count DESC


----------------------------------------------------------------------------------------------------
--	Continents with highest death rate per population
SELECT continent,  MAX( CAST( total_deaths AS int ) ) as Total_Death_Count
FROM [Portfolio Project]..Covid_Deaths
WHERE continent IS NOT NULL
GROUP BY continent
ORDER BY Total_Death_Count DESC


----------------------------------------------------------------------------------------------------
-- Global Numbers by Date
SELECT date, 
	SUM( new_cases ) as Total_Case_Count,
	SUM( CAST( new_deaths AS int ) ) as Total_Death_Count,
	(
	SUM(
		CASE
			WHEN new_deaths IS NULL
			THEN 0
			ELSE CAST( new_deaths AS int )
		END )
	/
	SUM(
		CASE
			WHEN new_cases IS NULL 
			THEN 0 
			ELSE new_cases
		END ) 
	) * 100 as Death_Percentage
FROM [Portfolio Project]..Covid_Deaths
WHERE continent IS NOT NULL
GROUP BY date
ORDER BY 1, 2


----------------------------------------------------------------------------------------------------
--	Global Numbers by Date
--	Same query as above but using SET methods to control query behavior to avoid errors
SET ARITHABORT OFF
SET ANSI_WARNINGS OFF
SELECT date, 
	SUM( new_cases ) as Total_Case_Count,
	SUM( CAST( new_deaths AS int ) ) as Total_Death_Count,
	SUM( CAST( new_deaths AS int ) ) / SUM( new_cases ) * 100 as Death_Percentage
FROM [Portfolio Project]..Covid_Deaths
WHERE continent IS NOT NULL
GROUP BY date
ORDER BY 1, 2


----------------------------------------------------------------------------------------------------
--	Total Global Numbers
SELECT 
	SUM( new_cases ) as Total_Case_Count,
	SUM( CAST( new_deaths AS int ) ) as Total_Death_Count,
	SUM( CAST( new_deaths AS int ) ) / SUM( new_cases ) * 100 as Death_Percentage
FROM [Portfolio Project]..Covid_Deaths
WHERE continent IS NOT NULL
ORDER BY 1, 2


----------------------------------------------------------------------------------------------------
--	Joining tables together
SELECT *
FROM [Portfolio Project].dbo.Covid_Deaths  cd
JOIN [Portfolio Project].dbo.Covid_Vaccinations  cv
	ON cd.location = cv.location
	AND cd.date = cv.date


----------------------------------------------------------------------------------------------------
--	Total population vs vaccinations
SELECT cd.continent, cd.location, cd.date, cd.population, cv.new_vaccinations,
	SUM( CONVERT( int, cv.new_vaccinations) ) OVER ( PARTITION BY cd.location ORDER BY cd.location, cd.date  ) as Total_Vaccination_Count,
	(SUM( CONVERT( int, cv.new_vaccinations) ) OVER ( PARTITION BY cd.location ORDER BY cd.location, cd.date  )/population) * 100 as Vaccination_Percentage
FROM [Portfolio Project].dbo.Covid_Deaths  cd
JOIN [Portfolio Project].dbo.Covid_Vaccinations  cv
	ON cd.location = cv.location
	AND cd.date = cv.date
WHERE cd.continent IS NOT NULL
ORDER BY 2, 3


----------------------------------------------------------------------------------------------------
--	Total population vs vaccinations
--	Same query as above using CTE (Common Table Expression) method
WITH POPvsVAC (continent, location, date, population,  new_vaccinations, Total_Vaccination_Count)
AS
(
SELECT cd.continent, cd.location, cd.date, cd.population, cv.new_vaccinations,
	SUM( CONVERT( int, cv.new_vaccinations) ) OVER ( PARTITION BY cd.location ORDER BY cd.location, cd.date  ) as Total_Vaccination_Count
FROM [Portfolio Project].dbo.Covid_Deaths  cd
JOIN [Portfolio Project].dbo.Covid_Vaccinations  cv
	ON cd.location = cv.location
	AND cd.date = cv.date
WHERE cd.continent IS NOT NULL
)
SELECT *, (Total_Vaccination_Count/population) * 100 as Vaccination_Percentage
FROM POPvsVAC
ORDER BY 2, 3


----------------------------------------------------------------------------------------------------
--	Total population vs vaccinations
--	Same query as above but using a TEMP TABLE method to insert into query
DROP TABLE IF EXISTS #Population_Vaccinated_Percentage
CREATE TABLE #Population_Vaccinated_Percentage
(
continent nvarchar(255),
location  nvarchar(255),
date datetime,
population numeric,
new_vaccinations numeric,
Total_Vaccination_Count numeric
)
INSERT INTO #Population_Vaccinated_Percentage
SELECT cd.continent, cd.location, cd.date, cd.population, cv.new_vaccinations,
	SUM( CONVERT( int, cv.new_vaccinations) ) OVER ( PARTITION BY cd.location ORDER BY cd.location, cd.date  ) as Total_Vaccination_Count
FROM [Portfolio Project].dbo.Covid_Deaths  cd
JOIN [Portfolio Project].dbo.Covid_Vaccinations  cv
	ON cd.location = cv.location
	AND cd.date = cv.date
WHERE cd.continent IS NOT NULL
SELECT *, (Total_Vaccination_Count/population) * 100 as Vaccination_Percentage
FROM #Population_Vaccinated_Percentage
ORDER BY 2, 3


----------------------------------------------------------------------------------------------------
--	Data to create a view for Data Visualizations
CREATE VIEW Population_Vaccinated_Percentage as
SELECT cd.continent, cd.location, cd.date, cd.population, cv.new_vaccinations,
	SUM( CONVERT( int, cv.new_vaccinations) ) OVER ( PARTITION BY cd.location ORDER BY cd.location, cd.date  ) as Total_Vaccination_Count
FROM [Portfolio Project].dbo.Covid_Deaths  cd
JOIN [Portfolio Project].dbo.Covid_Vaccinations  cv
	ON cd.location = cv.location
	AND cd.date = cv.date
WHERE cd.continent IS NOT NULL
