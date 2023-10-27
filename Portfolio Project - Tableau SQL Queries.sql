/*

Queries used for Tableau Project

*/



--	1.	
SELECT 
	SUM( new_cases ) as Total_Case_Count, 
	SUM( CAST( new_deaths AS int ) ) as Total_Death_Count, 
	SUM( CAST( new_deaths AS int ) ) / SUM( New_Cases ) * 100 as Death_Percentage
FROM [Portfolio Project].dbo.Covid_Deaths
--Where location like '%states%'
WHERE continent IS NOT NULL 
--Group By date
ORDER BY 1,2




--SELECT SUM( new_cases ) as Total_Cases, SUM( CAST( new_deaths AS int ) ) as Total_Deaths, SUM( CAST( new_deaths AS int ) ) / SUM( New_Cases ) * 100 as Death_Percentage
--From [Portfolio Project]..Covid_Deaths
----Where location like '%states%'
--where location = 'World'
----Group By date
--order by 1,2




--	2.
SELECT location, 
	SUM( CAST( new_deaths AS int ) ) as Total_Death_Count
FROM [Portfolio Project]..Covid_Deaths
--Where location like '%states%'
WHERE continent IS NULL 
	AND location NOT IN ('World', 'European Union', 'International')
GROUP BY location
ORDER BY Total_Death_Count DESC




--	3.
SELECT location, population, 
	MAX( total_cases ) as Highest_Infection_Count,  
	MAX( (total_cases/population) ) * 100 as Population_Infected_Percentage
FROM [Portfolio Project]..Covid_Deaths
--Where location like '%states%'
GROUP BY Location, Population
ORDER BY Population_Infected_Percentage DESC




--	4.
SELECT location, population, date, 
	MAX( total_cases ) as Highest_Infection_Count,  
	MAX( (total_cases/population) ) * 100 as Population_Infected_Percentage
FROM [Portfolio Project]..Covid_Deaths
--Where location like '%states%'
GROUP BY Location, Population, date
ORDER BY Population_Infected_Percentage DESC
