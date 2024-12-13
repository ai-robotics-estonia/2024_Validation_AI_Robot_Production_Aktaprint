*This is a template repository for this organization. Start by replacing the placeholder for the project name with its actual title.*

# [Creation and validation of a prototype of an AI-based software robot for automatic modelling, planning and optimization of production processes based on artificial intelligence in Aktaprint OÜ.]

## Summary
| Company Name | [Aktaprint OÜ](https://website.link) |
| :--- | :--- |
| Development Team Lead Name | [Tarmo Kadak](https://profile.link) |
| Development Team Lead E-mail | [tarmo.kadak@taltech.ee](mailto:email@example.com) |
| Duration of the Demonstration Project | 04/2024-12/2024
| Final Report | [LÕPPARUANNE,101224.pdf](https://github.com/user-attachments/files/18085693/LOPPARUANNE.101224.pdf)
 |

### Each project has an alternative for documentation
1. Fill in the [description](#description) directly in the README below *OR*;
2. make a [custom agreement with the AIRE team](#custom-agreement-with-the-AIRE-team).

# Description
## Objectives of the Demonstration Project
*Please describe your project objectives in detail.*

The goal of the project was to create and validate an AI-based software robot prototype designed for the most effective modelling and optimization of the company's various products and production processes. Within the entire core process of the company, the created robot is most closely related to sales and production planning activities, but it also has an impact on other activities. 
The task of the robot is to find a sufficiently good production process for a specific product/order throughout the entire order fulfilment period, starting from contacting the company with the customer's purchase request (including filling out the price offer (customer interface) form on the website), collecting the order requirements and ending with the production of the finished product that meets these requirements.
In the framework of this project, only the solution for creating an optimal print production process was implemented, which is an important module of the unified software system for customer management and production management planned in the future. Manufacturing process modelling based on artificial intelligence (software robot) provides solutions that help increase the efficiency, accuracy and overall performance of the manufacturing processes required by our company.

## Activities and Results of the Demonstration Project
### Challenge
*Please describe challenge addressed (i.e, whether and how the initial challenge was changed during the project, for which investment the demonstration project was provided).*

The database challenges and activities included:
• Identifying the data sources used and understanding the meaning of the data in them. The challenge was the lack of database documentation, therefore it was necessary to interview the creators of the database.
• Creating a copy of the company's operational database and simplifying it. Simplification meant removing unnecessary tables and columns from the database for this prototype.
• Improving the design quality of the created copy and, in turn, improving data quality, for example by changing column types and enforcing additional restrictions on data at the database level. The biggest challenge was transferring the data to the new structures. In the process, it was also necessary to convert the data, because numerical data were often in textual form in the source database. The challenge was that those filling the database with data had used different formats when presenting this data, and thus had to deal with extracting data values from texts using regular expressions. The multitude of formats meant that not all conversions could be fully automated. Creators of a new version of the company's database must take into account that it is also necessary to make manual conversions, and all automatically made conversions must be reviewed.
• The prototype to be created needed data about the machines and their characteristics. Among these data were some that were not previously registered in the database. Therefore, it was necessary to design a new sub-part of the database for storing data on machines and their properties.
• The created prototype generates a response based on the input data received from the customer's order. Thus, a database was designed where customer order data is entered.
• The communication between the different components of the created prototype was realized in an asynchronous way, which means that one part transmits a task to another without interrupting its work to wait for a response. A database was used for asynchronous data exchange, where one component stores the request in the created table, and the other component stores the response there after the end of the work.

The challenges and activities related to the development of artificial intelligence were as follows:
• Selecting the staple binder production process as the focus of the project.
• Choosing a back-to-front approach to problem analysis. The generation of the process starts with the finished order, and by generating the process, we try to reach the beginning of the production process - empty bows.
• Identification and understanding of bow assembly/pre-treatment as a production process bottleneck during interviews.
• By Brute Force, creating an algorithm that is guaranteed to find the optimal (cheapest) bow assembly solution and is the basis for the verification of artificial intelligence algorithms. A brute-force algorithm is based on recursively applying elementary operations to input pages to produce printable output arcs.
• Realization of the cost function of bow assembly/pretreatment to evaluate the goodness of the solution.
• Optimizing the performance of the Brute Force algorithm to enable practical use.
• Implementation of two artificial intelligence algorithms:
o Simulated Annealing
o Monte Carlo Tree Search. This algorithm was not originally mentioned, but during the work it turned out that it fits well with the recursive bow assembly approach.
• Verification of these AI algorithms based on the price function compared to a brute force algorithm. The gain in speed is astronomical for larger issues, the loss in price is acceptable.
• Tuning of artificial intelligence algorithms.
• Comparison of artificial intelligence algorithms. MCTS has a slight advantage.
• Evaluation of the expansion possibilities of artificial intelligence algorithms. They are stronger on the MCTS algorithm, which can be extended with various pre-trained machine learning models to evaluate the goodness of the solution branch a’la AlphaZero.

### Data Sources
*Please describe which data was used for the technological solution.*  
- [Source 1],
- [Source 2],
- etc... .

### AI Technologies
*Please describe and justify the use of selected AI technologies.*
- [AI technology 1],
- [AI technology 2],
- etc... .

### Technological Results
*Please describe the results of testing and validating the technological solution.*

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

### Technical Architecture
*Please describe the technical architecture (e.g, presented graphically, where the technical solution integration with the existing system can also be seen).*
- [Component 1],
- [Component 2], 
- etc... .

![backend-architecture](https://github.com/ai-robotics-estonia/_project_template_/assets/15941300/6d405b21-3454-4bd3-9de5-d4daad7ac5b7)


### User Interface 
*Please describe the details about the user interface(i.e, how does the client 'see' the technical result, whether a separate user interface was developed, command line script was developed, was it validated as an experiment, can the results be seen in ERP or are they integrated into work process)*

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

### Future Potential of the Technical Solution
*Please describe the potential areas for future use of the technical solution.*
- [Use case 1],
- [Use case 2],
- etc... .

### Lessons Learned
*Please describe the lessons learned (i.e. assessment whether the technological solution actually solved the initial challenge).*

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

# Custom agreement with the AIRE team
*If you have a unique project or specific requirements that don't fit neatly into the Docker file or description template options, we welcome custom agreements with our AIRE team. This option allows flexibility in collaborating with us to ensure your project's needs are met effectively.*

*To explore this option, please contact our demonstration projects service manager via katre.eljas@taltech.ee with the subject line "Demonstration Project Custom Agreement Request - [Your Project Name]." In your email, briefly describe your project and your specific documentation or collaboration needs. Our team will promptly respond to initiate a conversation about tailoring a solution that aligns with your project goals.*
