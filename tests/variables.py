from models.ObjectId import PydanticObjectId
import datetime


STATIC_USER_DICT = {
    "_id": PydanticObjectId(),
    "createdAt": datetime.datetime.fromtimestamp(1625140392353/1000),
    "updatedAt": datetime.datetime.fromtimestamp(1625162913532/1000),
    "spotifyAuthDetails": {
        "access_token": "BQDus8iqYZRDo1mg9AD8Y_D5T1-67h_09my5-NdoaXvtiM9our85OHH0s7-0SDITqW8TWq29Lbu0UNpEXTyrqAPYLtxLZMBKq11kZ_q9M29dKG3bUeq4JGBCCcB2RBhtTZe60jIbzsxVc0CNhjF-rzXSuvS2pjPNejV2dDcHkgEPphfhA7ciOY-UGzJ9Q5eyEe9nvB-fBlSh0s1eK8tbuP7xoJMjXt2vH6UoBwWm-Q",
        "refresh_token": "AQA23A-iAh8WT-ldGcu8fuwSY5jhJbNldtjdlV9feO0mqrWIubTCmwXusX0c-fH4qj3nEke65D3WqGTnMOeFnz3-ZYBx_RmePqa0T3vKRRaEkPPAlRa5Is7N2H9kxcgnEbg",
        "expires_in":  "3600",
        "expires_at": datetime.datetime.fromtimestamp(0),
        "token_type": "Bearer"
    },
    "user_id": "9yu91jbjo1p3e62a95h3z54o9",
    "settings": {
        "PlaylistNamingScheme": "MONTHLY"
    }
}
