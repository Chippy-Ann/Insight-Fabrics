<img width="1912" height="913" alt="image" src="https://github.com/user-attachments/assets/c7c68c9f-7614-4d52-903b-b307f52ca636" />
<img width="1902" height="973" alt="image" src="https://github.com/user-attachments/assets/3f360acc-1414-4125-b92b-7260ffeea10b" />
<img width="1906" height="873" alt="image" src="https://github.com/user-attachments/assets/c5011814-7e27-41ad-a47a-daa0d24dbdff" />

<img width="1917" height="933" alt="image" src="https://github.com/user-attachments/assets/8770b035-b07e-4f72-b73e-1d88f1dc24e0" />
<img width="1918" height="923" alt="image" src="https://github.com/user-attachments/assets/5ff50879-2b97-4f9d-bc16-37b9883133b9" />
<img width="1337" height="691" alt="image" src="https://github.com/user-attachments/assets/bf35abb2-8568-40da-9576-43d7361a1108" />

<img width="1491" height="842" alt="image" src="https://github.com/user-attachments/assets/54f89a39-83d3-4a51-a116-aefe6a92f125" />
<img width="1677" height="807" alt="image" src="https://github.com/user-attachments/assets/dc225f64-85b3-4d60-8182-53513f210de5" />
<img width="1782" height="915" alt="image" src="https://github.com/user-attachments/assets/58fcf5d0-e024-4d5d-bbe5-4b2b480217ed" />
<img width="1802" height="881" alt="image" src="https://github.com/user-attachments/assets/76ae05f5-e3f6-4476-8a64-4966a91722a5" />
<img width="1442" height="812" alt="image" src="https://github.com/user-attachments/assets/a9458c52-fd9e-49c0-84fe-e8d3a52ffb5b" />
<img width="1902" height="910" alt="image" src="https://github.com/user-attachments/assets/9b716c47-b111-4486-9dba-2ddc2547e9c7" />

<img width="1806" height="815" alt="image" src="https://github.com/user-attachments/assets/ee98b471-dc37-44c2-9424-49ba25d8ae91" />
<img width="531" height="215" alt="image" src="https://github.com/user-attachments/assets/332d84b0-b44c-49f5-880c-d0b35f4ccb00" />

## Measures :
Avg Burnout Score = AVERAGE(gold_burnout_daily_metrics[rolling_7d_negative_avg])
Avg Emotion Intensity = AVERAGE(emotion_trend_daily[avg_emotion_score])

High Burnout Count = 
CALCULATE(
    COUNTROWS(gold_burnout_daily_metrics),
    gold_burnout_daily_metrics[burnout_level] = "High"
)
High Burnout % = DIVIDE([High Burnout Count], COUNTROWS(gold_burnout_daily_metrics), 0)
Positive Sentiment % = 
CALCULATE(
    SUM(gold_sentiment_daily[sentiment_percentage]),
    gold_sentiment_daily[sentiment_bucket] = "Positive"
)
Total Records = COUNTROWS(gold_burnout_daily_metrics)


<img width="1785" height="901" alt="image" src="https://github.com/user-attachments/assets/7ed6b624-60c4-4f2d-9892-f6172c8fcdd2" />
<img width="1053" height="588" alt="image" src="https://github.com/user-attachments/assets/afc989b0-6906-4e99-ab3e-03464853aff8" />
<img width="418" height="838" alt="image" src="https://github.com/user-attachments/assets/b982ddc9-d682-4c90-8f85-b69d3c0f93de" />

<img width="1170" height="828" alt="image" src="https://github.com/user-attachments/assets/27b1585b-61c5-4e03-8715-e194caba0bf5" />
<img width="1176" height="820" alt="image" src="https://github.com/user-attachments/assets/a7cda8be-8a5a-4be1-b1ff-351617780cba" />

<img width="1876" height="921" alt="image" src="https://github.com/user-attachments/assets/ecc7714e-76f7-4c58-b58e-ac5e5cca9b56" />


<img width="1192" height="312" alt="image" src="https://github.com/user-attachments/assets/0a1b6225-d212-47eb-920e-00eafb2f2666" />
<img width="1132" height="657" alt="image" src="https://github.com/user-attachments/assets/d810f9de-9fa3-420f-b9dc-20aea2d794dc" />











