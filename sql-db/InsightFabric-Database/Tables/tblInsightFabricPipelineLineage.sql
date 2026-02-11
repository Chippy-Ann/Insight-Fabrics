CREATE TABLE tblInsightFabricPipelineLineage (
    LineageId        INT IDENTITY(1,1) PRIMARY KEY,
    RunId            VARCHAR(50)   NOT NULL,   -- Pipeline run identifier
    PipeLineName     VARCHAR(200)  NOT NULL,   
    CurrentStage      VARCHAR(200),
    BlobName         VARCHAR(200)  NOT NULL,   -- Filename returned by Function
    BlobUri          VARCHAR(500)  NOT NULL,   -- Full blob path
    SizeBytes        BIGINT         NULL,       -- File size in bytes
    CreatedOn        DATETIME       NULL,       -- Blob last modified timestamp

    -- Validation metrics
    RowCountRaw      INT            NULL,       -- Total rows ingested from Bronze
    RowCountSilver    INT            NULL,       -- Rows passing validation rules
    RowCountQuarrentine  INT            NULL,       -- Rows failing validation rules

    SilverModifiedOn DATETIME       NULL,       -- Last modified timestamp of Silver file/table

    -- Status tracking
    Status           VARCHAR(50)   NOT NULL DEFAULT('BronzeLoaded'), -- Pipeline stage
    ErrorMessage     NVARCHAR(500)  NULL        -- Capture errors if any
);