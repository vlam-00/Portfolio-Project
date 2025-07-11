/* user=vlam reportName=Portfolio Project - Data Cleaning in SQL reportSummary: Multiple queries written to display the different techniques used to clean data in SQL for my portfolio project */ 
----------------------------------------------------------------------------------------------------
-- Main Data Table

SELECT *
FROM [Portfolio Project].dbo.Nashville_Housing_Data_for_Data_Cleaning


----------------------------------------------------------------------------------------------------
--	Convert Date to YYYMM Format

SELECT SaleDate, CONVERT(nvarchar(6),SaleDate,112), FORMAT(SaleDate,'yyyyMM')
FROM [Portfolio Project].dbo.Nashville_Housing_Data_for_Data_Cleaning

/*
UPDATE Nashville_Housing_Data_for_Data_Cleaning
SET SaleDate = CONVERT(nvarchar(6),SaleDate,112)
*/

ALTER TABLE Nashville_Housing_Data_for_Data_Cleaning
ADD Sale_Year_Month int;

UPDATE Nashville_Housing_Data_for_Data_Cleaning
SET Sale_Year_Month = FORMAT(SaleDate,'yyyyMM')

/*	This was used to remove the first column I added, because I decided I wanted to differentiate my custom column from the original data.
ALTER TABLE Nashville_Housing_Data_for_Data_Cleaning
DROP COLUMN SaleYearMonth;
*/

SELECT SaleDate, Sale_Year_Month
FROM [Portfolio Project].dbo.Nashville_Housing_Data_for_Data_Cleaning


----------------------------------------------------------------------------------------------------
--	Populate Property Address Data for NULL Values

SELECT *
FROM [Portfolio Project].dbo.Nashville_Housing_Data_for_Data_Cleaning
--WHERE PropertyAddress is NULL
ORDER BY ParcelID

SELECT a.ParcelID, a.PropertyAddress, b.ParcelID, b.PropertyAddress, ISNULL(a.PropertyAddress, b.PropertyAddress)
FROM [Portfolio Project].dbo.Nashville_Housing_Data_for_Data_Cleaning a
JOIN [Portfolio Project].dbo.Nashville_Housing_Data_for_Data_Cleaning b
	ON a.ParcelID = b.ParcelID
	AND a.[UniqueID] <> b.[UniqueID]
WHERE a.PropertyAddress is NULL

UPDATE a
SET PropertyAddress = ISNULL(a.PropertyAddress, b.PropertyAddress)
FROM [Portfolio Project].dbo.Nashville_Housing_Data_for_Data_Cleaning a
JOIN [Portfolio Project].dbo.Nashville_Housing_Data_for_Data_Cleaning b
	ON a.ParcelID = b.ParcelID
	AND a.[UniqueID] <> b.[UniqueID]
WHERE a.PropertyAddress is NULL


----------------------------------------------------------------------------------------------------
--	Breaking out Address into Individual Columns (Street, City, State)

SELECT PropertyAddress
FROM [Portfolio Project].dbo.Nashville_Housing_Data_for_Data_Cleaning

SELECT
	SUBSTRING( PropertyAddress, 1, CHARINDEX(',', PropertyAddress)-1 ) as Street,
	SUBSTRING( PropertyAddress, CHARINDEX(',', PropertyAddress)+1 , LEN(PropertyAddress) ) as City
FROM [Portfolio Project].dbo.Nashville_Housing_Data_for_Data_Cleaning

ALTER TABLE Nashville_Housing_Data_for_Data_Cleaning
ADD Split_Street nvarchar(255);

UPDATE Nashville_Housing_Data_for_Data_Cleaning
SET Split_Street = SUBSTRING( PropertyAddress, 1, CHARINDEX(',', PropertyAddress)-1 )

ALTER TABLE Nashville_Housing_Data_for_Data_Cleaning
ADD Split_City nvarchar(255);

UPDATE Nashville_Housing_Data_for_Data_Cleaning
SET Split_City = SUBSTRING( PropertyAddress, CHARINDEX(',', PropertyAddress)+1 , LEN(PropertyAddress) )

SELECT PropertyAddress, Split_Street, Split_City
FROM [Portfolio Project].dbo.Nashville_Housing_Data_for_Data_Cleaning

SELECT OwnerAddress
FROM [Portfolio Project].dbo.Nashville_Housing_Data_for_Data_Cleaning

SELECT
	PARSENAME( REPLACE( OwnerAddress, ',', '.' ), 3 ),
	PARSENAME( REPLACE( OwnerAddress, ',', '.' ), 2 ),
	PARSENAME( REPLACE( OwnerAddress, ',', '.' ), 1 )
FROM [Portfolio Project].dbo.Nashville_Housing_Data_for_Data_Cleaning

ALTER TABLE Nashville_Housing_Data_for_Data_Cleaning
ADD Split_Owner_Street nvarchar(255);

UPDATE Nashville_Housing_Data_for_Data_Cleaning
SET Split_Owner_Street = PARSENAME( REPLACE( OwnerAddress, ',', '.' ), 3 )

ALTER TABLE Nashville_Housing_Data_for_Data_Cleaning
ADD Split_Owner_City nvarchar(255);

UPDATE Nashville_Housing_Data_for_Data_Cleaning
SET Split_Owner_City = PARSENAME( REPLACE( OwnerAddress, ',', '.' ), 2 )

ALTER TABLE Nashville_Housing_Data_for_Data_Cleaning
ADD Split_Owner_State nvarchar(255);

UPDATE Nashville_Housing_Data_for_Data_Cleaning
SET Split_Owner_State = PARSENAME( REPLACE( OwnerAddress, ',', '.' ), 1 )

SELECT OwnerAddress, Split_Owner_Street, Split_Owner_City, Split_Owner_State
FROM [Portfolio Project].dbo.Nashville_Housing_Data_for_Data_Cleaning


----------------------------------------------------------------------------------------------------
--	Change Y and N to Yes and No in "Sold as Vacant" Field

SELECT DISTINCT(SoldAsVacant), Count(SoldAsVacant)
FROM [Portfolio Project].dbo.Nashville_Housing_Data_for_Data_Cleaning
GROUP BY SoldAsVacant
ORDER BY 2

SELECT
	SoldAsVacant,
	CASE
		WHEN SoldAsVacant='Y' THEN 'Yes'
		WHEN SoldAsVacant='N' THEN 'No'
		ELSE SoldAsVacant
	END
FROM [Portfolio Project].dbo.Nashville_Housing_Data_for_Data_Cleaning

UPDATE Nashville_Housing_Data_for_Data_Cleaning
SET SoldAsVacant = 	CASE
						WHEN SoldAsVacant='Y' THEN 'Yes'
						WHEN SoldAsVacant='N' THEN 'No'
						ELSE SoldAsVacant
					END


----------------------------------------------------------------------------------------------------
--	Remove Duplicates

WITH Row_Num_CTE AS (
SELECT *,
	ROW_NUMBER() OVER (
		PARTITION BY ParcelID,
					 PropertyAddress,
					 SalePrice,
					 SaleDate,
					 LegalReference
		ORDER BY UniqueID
	) row_num
FROM [Portfolio Project].dbo.Nashville_Housing_Data_for_Data_Cleaning
)
DELETE
FROM Row_Num_CTE
WHERE row_num > 1


WITH Row_Num_CTE AS (
SELECT *,
	ROW_NUMBER() OVER (
		PARTITION BY ParcelID,
					 PropertyAddress,
					 SalePrice,
					 SaleDate,
					 LegalReference
		ORDER BY UniqueID
	) row_num
FROM [Portfolio Project].dbo.Nashville_Housing_Data_for_Data_Cleaning
)
SELECT * 
FROM Row_Num_CTE
WHERE row_num > 1
ORDER BY PropertyAddress


----------------------------------------------------------------------------------------------------
--	Delete Unused Columns

ALTER TABLE [Portfolio Project].dbo.Nashville_Housing_Data_for_Data_Cleaning
DROP COLUMN
	OwnerAddress, TaxDistrict, PropertyAddress

SELECT *
FROM [Portfolio Project].dbo.Nashville_Housing_Data_for_Data_Cleaning
