## Orthodox MMA Trainer

Orthodox MMA trainer is a web application which utilises pose estimation and computer vision to predict a user's technique / form in regards to certain strikes used within the sport of mixed martial arts, such as a jab. The goal of this project is to provide an inexpensive way for MMA enthusiasts and beginners alike to practice their striking technique. This is mainly aimed at beginners as it is important that they have good fundamentals before moving on to more complex techniques. It is important to note that the goal of this project is not to replace in person coaching, but to act as a tool for people with limited access to a MMA gym regularly or to be used in conjunction with in person training.

The web application accepts video as input and utilises Google’s latest lightweight pose estimation solution, BlazePose [1], to abstract the position of the user’s body in said video. These body landmarks are then fed into multiple classifiers, based on the inputted strike, and a feedback report is generated and displayed to the user. 

The web app is hosted on AWS at the domain [https://orthodoxmma.com]. 
