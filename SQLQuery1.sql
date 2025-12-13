-- LOADING THE DATA SET
select * from customer__churn

-- CORRECTING THE COLUMN NAME
EXEC sp_rename 'customer__churn.[Usage Frequency]', 'Usage_freq', 'COLUMN';
EXEC sp_rename 'customer__churn.[Payment Delay]', 'PaymentDelay', 'COLUMN';
EXEC sp_rename 'customer__churn.[Support Calls]', 'SupportCalls', 'COLUMN';
EXEC sp_rename 'customer__churn.[Subscription Type]', 'Subscription_Type', 'COLUMN';
EXEC sp_rename 'customer__churn.[Contract Length]', 'Contract_Length', 'COLUMN';
EXEC sp_rename 'customer__churn.[Total spend]', 'Total_spend', 'COLUMN';
EXEC sp_rename 'customer__churn.[Last Interaction]', 'Last_Interaction', 'COLUMN';

-- step 1
-- Handling missing values

SELECT *
FROM customer__churn
WHERE
     CustomerID     IS NULL OR
     Gender         IS NULL OR
     Age            IS NULL OR
     Tenure         IS NULL OR
	 Usage_freq is null or
     SupportCalls   IS NULL OR
     PaymentDelay   IS NULL OR
	 Subscription_Type is null or
	 Contract_Length is null or
     Total_Spend     IS NULL OR
     Last_Interaction IS NULL;

-- no missing value

--step 2
-- checking for duplicate values

SELECT CustomerID, COUNT(*) AS CountDuplicate
FROM customer__churn
GROUP BY CustomerID
HAVING COUNT(*) > 1;

-- no duplicate values

-- step 3
-- checking for  Data Types
SELECT COLUMN_NAME, DATA_TYPE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'customer__churn';

-- NOW CHANGE IN DATA TYPE
ALTER TABLE customer__churn
ALTER COLUMN Age FLOAT;

ALTER TABLE customer__churn
ALTER COLUMN Tenure FLOAT;

ALTER TABLE customer__churn
ALTER COLUMN Usage_freq FLOAT;

ALTER TABLE customer__churn
ALTER COLUMN SupportCalls FLOAT;

ALTER TABLE customer__churn
ALTER COLUMN PaymentDelay FLOAT;

ALTER TABLE customer__churn
ALTER COLUMN Total_spend FLOAT;

ALTER TABLE customer__churn
ALTER COLUMN Last_Interaction FLOAT;

ALTER TABLE customer__churn
ALTER COLUMN Churn FLOAT;

ALTER TABLE customer__churn
ALTER COLUMN CustomerID INT;


-- STEP 4
-- REMOVING ROW WITH EMPTY ENTRIES
DELETE  FROM customer__churn
where Subscription_Type ='';

-- step 5
-- checking balance in categorical data set and Out-of-domain Values 
SELECT Gender, COUNT(*) FROM customer__churn GROUP BY Gender;
SELECT Subscription_Type, COUNT(*) FROM customer__churn GROUP BY Subscription_Type;
SELECT Contract_Length, COUNT(*) FROM customer__churn GROUP BY Contract_Length;

--STEP 6
-- CHECKING FOR OUTLIERS 

WITH calc AS (
    SELECT
        -- AGE
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY Age) OVER () AS Age_Q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY Age) OVER () AS Age_Q3,

        -- TENURE
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY Tenure) OVER () AS Tenure_Q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY Tenure) OVER () AS Tenure_Q3,

        -- USAGE FREQ
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY Usage_freq) OVER () AS UF_Q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY Usage_freq) OVER () AS UF_Q3,

        -- SUPPORT CALLS
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY SupportCalls) OVER () AS SC_Q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY SupportCalls) OVER () AS SC_Q3,

        -- PAYMENT DELAY
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY PaymentDelay) OVER () AS PD_Q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY PaymentDelay) OVER () AS PD_Q3,

        -- TOTAL SPEND
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY Total_spend) OVER () AS TS_Q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY Total_spend) OVER () AS TS_Q3,

        -- LAST INTERACTION
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY Last_Interaction) OVER () AS LI_Q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY Last_Interaction) OVER () AS LI_Q3,

        -- CHURN
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY Churn) OVER () AS Churn_Q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY Churn) OVER () AS Churn_Q3
    FROM customer__churn   -- ✅ THIS WAS MISSING EARLIER
)
,
bounds AS (
    SELECT DISTINCT
        Age_Q1, Age_Q3,
        Age_Q1 - 1.5 * (Age_Q3 - Age_Q1) AS Age_LB,
        Age_Q3 + 1.5 * (Age_Q3 - Age_Q1) AS Age_UB,

        Tenure_Q1, Tenure_Q3,
        Tenure_Q1 - 1.5 * (Tenure_Q3 - Tenure_Q1) AS Tenure_LB,
        Tenure_Q3 + 1.5 * (Tenure_Q3 - Tenure_Q1) AS Tenure_UB,

        UF_Q1, UF_Q3,
        UF_Q1 - 1.5 * (UF_Q3 - UF_Q1) AS UF_LB,
        UF_Q3 + 1.5 * (UF_Q3 - UF_Q1) AS UF_UB,

        SC_Q1, SC_Q3,
        SC_Q1 - 1.5 * (SC_Q3 - SC_Q1) AS SC_LB,
        SC_Q3 + 1.5 * (SC_Q3 - SC_Q1) AS SC_UB,

        PD_Q1, PD_Q3,
        PD_Q1 - 1.5 * (PD_Q3 - PD_Q1) AS PD_LB,
        PD_Q3 + 1.5 * (PD_Q3 - PD_Q1) AS PD_UB,

        TS_Q1, TS_Q3,
        TS_Q1 - 1.5 * (TS_Q3 - TS_Q1) AS TS_LB,
        TS_Q3 + 1.5 * (TS_Q3 - TS_Q1) AS TS_UB,

        LI_Q1, LI_Q3,
        LI_Q1 - 1.5 * (LI_Q3 - LI_Q1) AS LI_LB,
        LI_Q3 + 1.5 * (LI_Q3 - LI_Q1) AS LI_UB,

        Churn_Q1, Churn_Q3,
        Churn_Q1 - 1.5 * (Churn_Q3 - Churn_Q1) AS Churn_LB,
        Churn_Q3 + 1.5 * (Churn_Q3 - Churn_Q1) AS Churn_UB
    FROM calc
)

SELECT c.*
FROM customer__churn c
CROSS JOIN bounds b
WHERE 
      c.Age             < b.Age_LB      OR c.Age             > b.Age_UB
   OR c.Tenure          < b.Tenure_LB   OR c.Tenure          > b.Tenure_UB
   OR c.Usage_freq      < b.UF_LB       OR c.Usage_freq      > b.UF_UB
   OR c.SupportCalls    < b.SC_LB       OR c.SupportCalls    > b.SC_UB
   OR c.PaymentDelay    < b.PD_LB       OR c.PaymentDelay    > b.PD_UB
   OR c.Total_spend     < b.TS_LB       OR c.Total_spend     > b.TS_UB
   OR c.Last_Interaction < b.LI_LB      OR c.Last_Interaction > b.LI_UB
   OR c.Churn           < b.Churn_LB    OR c.Churn           > b.Churn_UB;

-- There is no outleirs in the dataset

-- step 7
-- Encoding of dataset

-- Label encoding
ALTER TABLE customer__churn
ADD Gender_Label INT;

UPDATE customer__churn
SET Gender_Label = CASE 
    WHEN Gender = 'Male' THEN 1
    WHEN Gender = 'Female' THEN 0
    ELSE NULL
END;

-- OHE 
ALTER TABLE customer__churn
ADD Sub_Basic INT,
    Sub_Standard INT,
    Sub_Premium INT;

UPDATE customer__churn
SET 
    Sub_Basic = CASE WHEN Subscription_Type = 'Basic' THEN 1 ELSE 0 END,
    Sub_Standard = CASE WHEN Subscription_Type = 'Standard' THEN 1 ELSE 0 END,
    Sub_Premium = CASE WHEN Subscription_Type = 'Premium' THEN 1 ELSE 0 END;


-- encoding of contract length

ALTER TABLE customer__churn
ADD Contract_Length_Num INT;

UPDATE customer__churn
SET Contract_Length_Num = CASE
    WHEN Contract_Length = 'Annual' THEN 12
    WHEN Contract_Length = 'Quarterly' THEN 3
    WHEN Contract_Length = 'Monthly' THEN 1
    ELSE NULL
END;


ALTER TABLE customer__churn
DROP COLUMN Gender, Subscription_Type, Contract_Length;


-- standarding the Contract_Length_Num
ALTER TABLE customer__churn 
ADD Contract_Length_std FLOAT;

UPDATE customer__churn
SET Contract_Length_std =
    (Contract_Length_Num - (SELECT AVG(Contract_Length_Num) FROM customer__churn)) /
    NULLIF((SELECT STDEV(Contract_Length_Num) FROM customer__churn), 0);

ALTER TABLE customer__churn
DROP COLUMN Contract_Length_Num

select * from customer__churn