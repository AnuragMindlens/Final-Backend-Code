mappings = {
    "questions": [
        {
            "category": "seated_posture",
            "items": [
                {
                    "id": "1",
                    "scenarios": {
                        "negative": {
                            "risk": "Medium",
                            "affected_parts": ["Lower back"],
                            "conditions": ["Lower back pain", "Herniated disk"],
                            "current": "You're sitting back but slouching in your chair.",
                            "current_summary": "Slouching back",
                            "recommendation": "Sit fully back in your chair, ensuring the backrest supports your spine.",
                            "recommendation_summary": "Sit fully back",
                            "image_path": "aipose/For AI report/Inline with desk.jpg"
                        },
                        "positive": {
                            "risk": "High",
                            "affected_parts": ["Lower back"],
                            "conditions": ["Lower back pain", "Herniated disk"],
                            "current": "You're leaning forward, leaving your back unsupported.",
                            "current_summary": "Leaning forward unsupported",
                            "recommendation": "Sit fully back in your chair, ensuring the backrest supports your spine.",
                            "recommendation_summary": "Backrest supports spine",
                            "image_path": "aipose/For AI report/Inline with desk.jpg"
                        },
                        "neutral": {
                            "risk": "Low",
                            "affected_parts": ["Lower back"],
                            "conditions": [""],
                            "current": "Your seating position keeps your back adequately supported.",
                            "current_summary": "Back supported",
                            "recommendation": "",
                            "recommendation_summary": "",
                            "image_path": ""
                        }
                    }
                },
                {
                    "id": "2",
                    "scenarios": {
                        "negative": {
                            "risk": "High",
                            "affected_parts": ["Knees", "Lower back"],
                            "conditions": ["Knee pain", "Lower back pain", "Herniated disk"],
                            "current": "You are sitting too low. This puts pressure on the spine as it is being compressed.",
                            "current_summary": "Sitting too low",
                            "recommendation": "Sit high such that your hips are slightly higher than your knees with feet supported. Adjust your chair or sit on top of a cushion to get the desired height. If your feet are hanging, use a footrest or box for support.",
                            "recommendation_summary": "Raise hips supported",
                            "image_path": "aipose/For AI report/Inline with desk.jpg"
                        },
                        "positive": {
                            "risk": "Medium",
                            "affected_parts": ["Lower back"],
                            "conditions": ["Lower back pain", "Herniated disk (with prolonged sitting)"],
                            "current": "While sitting with hips in-line with the knees creates a 90° angle, it is not the right angle for you!",
                            "current_summary": "Hips 90° angle",
                            "recommendation": "Sit high such that your hips are slightly higher than your knees with feet supported. Adjust your chair or sit on top of a cushion to get the desired height. If your feet are hanging, use a footrest or box for support.",
                            "recommendation_summary": "Raise hips supported",
                            "image_path": "aipose/For AI report/Inline with desk.jpg"
                        },
                        "neutral": {
                            "risk": "Low",
                            "affected_parts": ["Lower back"],
                            "conditions": [""],
                            "current": "You are sitting at a good height to reduce pressure on the spine. Ensure your feet are well supported.",
                            "current_summary": "Good height supported",
                            "recommendation": "",
                            "recommendation_summary": "",
                            "image_path": ""
                        }
                    }
                }
            ]
        },
        {
            "category": "hand_position",
            "items": [
                {
                    "id": "1",
                    "scenarios": {
                        "negative": {
                            "risk": "Medium",
                            "affected_parts": ["Wrist"],
                            "conditions": ["Tendinitis"],
                            "current": "Your wrists flexed downwards while typing, it can strain the tendons at the back of your hand, increasing the risk of discomfort and repetitive strain injuries.",
                            "current_summary": "Wrists flexed downwards",
                            "recommendation": "Ensure your keyboard is positioned about a palm's distance from the edge of the table, maintaining a neutral posture. This setup reduces wrist stress and encourages better posture. Keeping your wrists in a neutral position while typing ensures minimal strain, promoting long-term comfort and reducing the risk of repetitive stress injuries.",
                            "recommendation_summary": "Neutral posture keyboard",
                            "image_path": ""
                        },
                        "positive": {
                            "risk": "Medium",
                            "affected_parts": ["Wrist"],
                            "conditions": ["Carpal tunnel syndrome"],
                            "current": "Your wrists are flexed upwards while typing, it can increase tension in the tendons and nerves, potentially leading to conditions like carpal tunnel syndrome.",
                            "current_summary": "Wrists flexed upwards",
                            "recommendation": "Ensure your keyboard is positioned about a palm's distance from the edge of the table, maintaining a neutral posture. This setup reduces wrist stress and encourages better posture. Keeping your wrists in a neutral position while typing ensures minimal strain, promoting long-term comfort and reducing the risk of repetitive stress injuries.",
                            "recommendation_summary": "Neutral posture keyboard",
                            "image_path": ""
                        },
                        "neutral": {
                            "risk": "Low",
                            "affected_parts": ["Wrist"],
                            "conditions": [""],
                            "current": "Your wrists in a neutral position while typing ensures minimal strain, promoting long-term comfort and reducing the risk of repetitive stress injuries.",
                            "current_summary": "Neutral wrist position",
                            "recommendation": "",
                            "recommendation_summary": "",
                            "image_path": ""
                        }
                    }
                },
                {
                    "id": "2",
                    "scenarios": {
                        "negative": {
                            "risk": "Medium",
                            "affected_parts": ["Wrist"],
                            "conditions": ["Tendinitis"],
                            "current": "Your current grip makes an arched positioning of the fingers, this can lead to finger strain over extended periods, especially if pressing the buttons with force.",
                            "current_summary": "Arched finger grip",
                            "recommendation": "Use an ergonomically designed keyboard that fits comfortably in your hand. Consider using a mouse pad with a wrist rest to support your hand and wrist. Take regular breaks, stretch your fingers, and practice a relaxed hand grip to reduce strain and enhance comfort.",
                            "recommendation_summary": "Ergonomic keyboard grip",
                            "image_path": "aipose/For AI report/Mouse_Relaxed hand.jpg"
                        },
                        "positive": {
                            "risk": "Medium",
                            "affected_parts": ["Hand"],
                            "conditions": ["Tennis elbow"],
                            "current": "Your current way of mousing can lead to finger fatigue quicker since you're using only your fingertips.",
                            "current_summary": "Using fingertips mouse",
                            "recommendation": "Use an ergonomically designed mouse that fits comfortably in your hand. Consider using a mouse pad with a wrist rest to support your hand and wrist. Take regular breaks, stretch your fingers, and practice a relaxed hand grip to reduce strain and enhance comfort.",
                            "recommendation_summary": "Ergonomic mouse grip",
                            "image_path": "aipose/For AI report/Mouse_Relaxed hand.jpg"
                        },
                        "neutral": {
                            "risk": "Low",
                            "affected_parts": ["Wrist"],
                            "conditions": [""],
                            "current": "Your wrists in a neutral position while using the keyboard ensures minimal strain, promoting long-term comfort and reducing the risk of repetitive stress injuries.",
                            "current_summary": "Neutral wrist position",
                            "recommendation": "",
                            "recommendation_summary": "",
                            "image_path": ""
                        }
                    }
                },
                {
                    "id": "3",
                    "scenarios": {
                        "negative": {
                            "risk": "High",
                            "affected_parts": ["Wrist"],
                            "conditions": ["Carpal tunnel syndrome"],
                            "current": "Your wrists are twisted while using the keyboard, it can lead to uneven pressure on the wrist structures, potentially causing discomfort and increasing the likelihood of wrist-related ailments.",
                            "current_summary": "Twisted wrist keyboard",
                            "recommendation": "Ensure your keyboard is positioned about a palm's distance from the edge of the table, maintaining a neutral posture. This setup reduces wrist stress and encourages better posture. Keeping your wrists in a neutral position while using the mouse ensures minimal strain, promoting long-term comfort and reducing the risk of repetitive stress injuries.",
                            "recommendation_summary": "Neutral posture keyboard",
                            "image_path": "aipose/For AI report/Keyboard_Neutral wrist position.jpg"
                        },
                        "positive": {
                            "risk": "High",
                            "affected_parts": ["Wrist"],
                            "conditions": ["Carpal tunnel syndrome"],
                            "current": "Your wrists are twisted while using the keyboard, it can lead to uneven pressure on the wrist structures, potentially causing discomfort and increasing the likelihood of wrist-related ailments.",
                            "current_summary": "Twisted wrist keyboard",
                            "recommendation": "Ensure your keyboard is positioned about a palm's distance from the edge of the table, maintaining a neutral posture. This setup reduces wrist stress and encourages better posture. Keeping your wrists in a neutral position while using the mouse ensures minimal strain, promoting long-term comfort and reducing the risk of repetitive stress injuries.",
                            "recommendation_summary": "Neutral posture keyboard",
                            "image_path": "aipose/For AI report/Keyboard_Neutral wrist position.jpg"
                        },
                        "neutral": {
                            "risk": "Low",
                            "affected_parts": ["Wrist"],
                            "conditions": [""],
                            "current": "Your wrists in a neutral position while using the mouse ensures minimal strain, promoting long-term comfort and reducing the risk of repetitive stress injuries.",
                            "current_summary": "Neutral wrist position",
                            "recommendation": "",
                            "recommendation_summary": "",
                            "image_path": ""
                        }
                    }
                }
            ]
        },
        {
            "category": "desk_position",
            "items": [
                {
                    "id": "1",
                    "scenarios": {
                        "negative": {
                            "risk": "High",
                            "affected_parts": ["Shoulders", "Neck", "Upper back", "Arms"],
                            "conditions": ["Cervical spondylosis", "Thoracic outlet syndrome"],
                            "current": "Your desk is too high; elbows are low, lifting arms and shoulders during typing.",
                            "current_summary": "Desk too high",
                            "recommendation": "Align your desk height with your elbow to ensure your arms and shoulders remain relaxed during work.",
                            "recommendation_summary": "Align desk height",
                            "image_path": "aipose/For AI report/Hips higher-1.jpg"
                        },
                        "positive": {
                            "risk": "High",
                            "affected_parts": ["Shoulders", "Neck", "Upper back", "Arms"],
                            "conditions": ["Cervical spondylosis", "Thoracic outlet syndrome"],
                            "current": "Your desk is too low; elbows are high, causing a forward lean to type.",
                            "current_summary": "Desk too low",
                            "recommendation": "Align your desk height with your elbow to ensure your arms and shoulders remain relaxed during work.",
                            "recommendation_summary": "Align desk height",
                            "image_path": "aipose/For AI report/Hips higher-1.jpg"
                        },
                        "neutral": {
                            "risk": "Low",
                            "affected_parts": ["Lower back"],
                            "conditions": [""],
                            "current": "Your desk is at the right height; elbows align, arms and shoulders relaxed.",
                            "current_summary": "Right desk height",
                            "recommendation": "",
                            "recommendation_summary": "",
                            "image_path": ""
                        }
                    }
                },
                {
                    "id": "2",
                    "scenarios": {
                        "negative": {
                            "risk": "High",
                            "affected_parts": ["Neck", "Shoulders", "Upper back", "Lower back"],
                            "conditions": ["Cervical spondylosis", "Thoracic outlet syndrome", "Lower back pain", "Herniated disc"],
                            "current": "Screen is too low; you lean forward, losing back support and risking upper back and shoulder pain.",
                            "current_summary": "Screen too low",
                            "recommendation": "Adjust your Screen using a stand or books so the first line of text aligns with eye level. This alignment helps prevent neck and upper back strain.",
                            "recommendation_summary": "Raise Screen height",
                            "image_path": "aipose/For AI report/Screen-at eye level.jpg"
                        },
                        "positive": {
                            "risk": "Medium",
                            "affected_parts": ["Neck", "Head"],
                            "conditions": ["Cervical spondylosis"],
                            "current": "Screen is too high; you tilt your head up, tightening neck muscles and increasing the risk of cervical spondylosis.",
                            "current_summary": "Screen too high",
                            "recommendation": "Adjust your Screen using a stand or books so the first line of text aligns with eye level. This alignment helps prevent neck and upper back strain.",
                            "recommendation_summary": "Lower Screen height",
                            "image_path": "aipose/For AI report/Screen-at eye level.jpg"
                        },
                        "neutral": {
                            "risk": "Low",
                            "affected_parts": ["Neck"],
                            "conditions": [""],
                            "current": "Your Screen is at eye level, promoting good posture and minimizing neck and upper back strain.",
                            "current_summary": "Screen eye level",
                            "recommendation": "",
                            "recommendation_summary": "",
                            "image_path": ""
                        }
                    }
                },
                {
                    "id": "3",
                    "scenarios": {
                        "negative": {
                            "risk": "Medium",
                            "affected_parts": ["Wrist"],
                            "conditions": ["Carpal tunnel syndrome"],
                            "current": "Your keyboard and mouse are placed too close, or you are sitting too close to them. This leaves you with no room to stay relaxed, causing you to hunch over. This position can lead to poor posture, resulting in strain on your neck and back, as well as discomfort.",
                            "current_summary": "Sitting too close/Cramped position",
                            "recommendation": "Position your chair at a proper distance from your desk, allowing you to sit back comfortably with your back supported. Ensure your keyboard and mouse are placed so your elbows remain at a 90-degree angle and at a palm's distance from the edge of the table to avoid contact stress.",
                            "recommendation_summary": "Sit farther away/ move the setup away",
                            "image_path": "aipose/For AI report/keyboard-mouse-position.jpg"
                        },
                        "positive": {
                            "risk": "High",
                            "affected_parts": ["Elbows", "Shoulders", "Arms", "Wrist", "Upper back"],
                            "conditions": ["Cubittal tunnel syndrome", "Carpal tunnel syndrome", "Thoracic outlet syndrome"],
                            "current": "Your keyboard and mouse are placed too far, or if you are sitting too far from them, Due to this you may need to extend your arms to type/mouse. This can lead to shoulder and upper back strain, as well as discomfort in the arms and wrists. Over time, this position can cause fatigue and increase the likelihood of developing issues.",
                            "current_summary": "Sitting too far/Extending to reach",
                            "recommendation": "Move your keyboard and mouse closer to you, ensuring they are within easy reach without having to stretch your arms. Adjust your chair so your elbows remain close to a 90-degree angle and place the keyboard and mouse at a palm's distance from the edge of the table to avoid contact stress.",
                            "recommendation_summary": "Sit closer/Bring mouse closer",
                            "image_path": "aipose/For AI report/keyboard-mouse-position.jpg"
                        },
                        "neutral": {
                            "risk": "Low",
                            "affected_parts": [""],
                            "conditions": [""],
                            "current": "Hip-neck line and the neck-elbow line are close to each other",
                            "current_summary": "Relaxed setup",
                            "recommendation": "",
                            "recommendation_summary": "",
                            "image_path": ""
                        }
                    }
                }
            ]
        },
        {
            "category": "image_annotation",
            "items": [
                {
                    "id": "1",
                    "scenarios": {
                        "negative": {
                            "risk": "Low",
                            "affected_parts": ["Eyes", "Neck", "Head"],
                            "conditions": ["Eye strain", "Neck strain", "Migraine"],
                            "current": "Your screen is too close, leading to potential eye strain and excessive head and neck movement.",
                            "current_summary": "Screen too close",
                            "recommendation": "Your screen is too close, leading to potential eye strain and excessive head and neck movement.",
                            "recommendation_summary": "Move screen back",
                            "image_path": "aipose/For AI report/Screen-at arm's length.jpg"
                        },
                        "positive": {
                            "risk": "High",
                            "affected_parts": ["Upper back", "Lower back", "Shoulders", "Arms"],
                            "conditions": ["Cervical spondylosis", "Thoracic outlet syndrome", "Low back pain", "Herniated disc"],
                            "current": "Your screen is too far, causing a tendency to lean in.",
                            "current_summary": "Screen too far",
                            "recommendation": "Position your Screen an arm's length away. Bring it closer only if reading becomes difficult.",
                            "recommendation_summary": "Move screen closer",
                            "image_path": "aipose/For AI report/Screen-at arm's length.jpg"
                        },
                        "neutral": {
                            "risk": "Low",
                            "affected_parts": [""],
                            "conditions": [""],
                            "current": "You have an optimal viewing distance; use an external keyboard and mouse for relaxed arms and shoulders.",
                            "current_summary": "Optimal viewing distance",
                            "recommendation": "",
                            "recommendation_summary": "",
                            "image_path": ""
                        }
                    }
                },
                {
                    "id": "2",
                    "scenarios": {
                        "negative": {
                            "risk": "High",
                            "affected_parts": ["Eyes"],
                            "conditions": ["Eye strain"],
                            "current": "You are sitting too close to the desk.",
                            "current_summary": "Too close to desk",
                            "recommendation": "Move further away from the desk.",
                            "recommendation_summary": "Move further away",
                            "image_path": "aipose/For AI report/Screen-at arm's length.jpg"
                        },
                        "positive": {
                            "risk": "Low",
                            "affected_parts": ["Eyes"],
                            "conditions": ["Eye strain"],
                            "current": "You are sitting too far from the desk",
                            "current_summary": "Too far",
                            "recommendation": "Sit closer to the desk",
                            "recommendation_summary": "Sit closer",
                            "image_path": "aipose/For AI report/Screen-at arm's length.jpg"
                        },
                        "neutral": {
                            "risk": "Low",
                            "affected_parts": [""],
                            "conditions": [""],
                            "current": "The annotation color scheme is adequate, but there is room for improvement.",
                            "current_summary": "Adequate color scheme",
                            "recommendation": "Consider using more distinct colors to further enhance clarity.",
                            "recommendation_summary": "Use distinct colors",
                            "image_path": ""
                        }
                    }
                }
            ]
        },
    ]
}
