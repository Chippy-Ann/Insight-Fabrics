CREATE PROC SpInsertLineage
(
@RunId              VARCHAR(50) ,
@PipeLineName       VARCHAR(200),
@CurrentStage       VARCHAR(20),
@BlobName           VARCHAR(200),
@BlobUri            VARCHAR(200),
@SizeBytes          BIGINT,
@CreatedOn          DATETIME,
@RowCountRaw        INT,
@RowCountSilver      INT,
@RowCountQuarrentine INT,
@SilverModifiedOn    DATETIME,
@Status             VARCHAR(50),
@ErrorMessage       NVARCHAR(500)
)
AS
BEGIN
IF EXISTS (SELECT 1 FROM tblInsightFabricPipelineLineage 
    WHERE BlobName=@BlobName and BlobUri=@BlobUri )

    BEGIN
        UPDATE tblInsightFabricPipelineLineage
        SET RowCountSilver=@RowCountSilver
            ,RowCountQuarrentine=@RowCountQuarrentine
            ,Status=@Status
            ,ErrorMessage=@ErrorMessage
            ,CurrentStage=@CurrentStage
            ,PipeLineName=@PipeLineName
            ,SilverModifiedOn=@SilverModifiedOn

        WHERE BlobName=@BlobName and BlobUri=@BlobUri
    END
ELSE
    BEGIN
        Insert into tblInsightFabricPipelineLineage
        (    RunId, PipeLineName, CurrentStage, BlobName, BlobUri,
            SizeBytes, CreatedOn, RowCountRaw, RowCountSilver,
            RowCountQuarrentine, SilverModifiedOn, Status, ErrorMessage)
         values 
                (@RunId,@PipeLineName,@CurrentStage,@BlobName,@BlobUri
                ,@SizeBytes,@CreatedOn,@RowCountRaw 
                ,@RowCountSilver,@RowCountQuarrentine,@SilverModifiedOn
                ,@Status,@ErrorMessage)

    END

END