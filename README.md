*This is a template repository for this organization. Start by replacing the placeholder for the project name with its actual title.*

# [Adjustment and validation of a prototype of an AI-based software robot for automatic modelling, planning and optimization of production processes based on artificial intelligence in Aktaprint OÜ.]

## Summary
| Company Name | [Aktaprint OÜ](https://website.link) |
| :--- | :--- |
| Development Team Lead Name | [Tarmo Kadak](https://profile.link) |
| Development Team Lead E-mail | [tarmo.kadak@taltech.ee](mailto:email@example.com) |
| Duration of the Demonstration Project | 04/2024-12/2024
| Final Report | [LÕPPARUANNE,101224.pdf](https://github.com/user-attachments/files/18128024/LOPPARUANNE.101224.pdf)


### Each project has an alternative for documentation
1. Fill in the [description](#description) directly in the README below *OR*;
2. make a [custom agreement with the AIRE team](#custom-agreement-with-the-AIRE-team).

# Description
## Objectives of the Demonstration Project
*Please describe your project objectives in detail.*

The objective of the project was to test and validate an AI-based prototype of a software robot designed for the effective modeling and optimization of various products and production processes within the company. Throughout the entire core process of the company, the created robot is most closely associated with sales and production planning activities, while also influencing other functions. 
The robot’s task is to identify a sufficiently effective production process for a specific product or order over the entire order fulfillment period — from the moment a customer expresses purchase interest by contacting the company (including by filling out the price offer form on the website), to gathering order requirements, and culminating in the production of a finished product that meets those requirements. 
Within the scope of this project, only the solution for establishing an optimal print production process was implemented, which is an important module of the unified software system for customer management and production management planned for the future. 
Furthermore, AI-based (software robot-based) modeling of production processes offers solutions that help increase the efficiency, accuracy, and overall performance of the production processes required by our company. 

## Activities and Results of the Demonstration Project
### Challenge
*Please describe challenge addressed (i.e, whether and how the initial challenge was changed during the project, for which investment the demonstration project was provided).*

The database challenges and activities included:
- Identification of the data sources and understanding the meaning of the data contained within them. A major challenge was the lack of database documentation, which required interviewing the database creators.
- Creating a copy of the company’s operational database and simplifying it. For the purposes of this prototype, simplification meant removing unnecessary tables and columns from the database. 
- Improving the design quality of the created copy, and consequently the data quality, by, for example, changing column types and enforcing additional data constraints at the database level. The greatest challenge was transferring the data into new structures. In the process, it was also necessary to convert data since in the source database numeric data were often stored in textual form. The challenge was that those entering data into the database used different formats, so it was necessary to extract data values from text using regular expressions. The variety of formats meant that not all conversions could be fully automated. The creators of the company’s new database version must take into account that manual conversions are also necessary, and all automatically performed conversions must be reviewed. 
- The prototype required data on machines and their properties. Among these were also items that were not previously recorded in the database. Therefore, it was necessary to adjust a new database submodule for storing data on machines and their properties. 
- The prototype generates a response based on the input data received from the customer’s order. Accordingly, a database was adjusted into which customer order data is entered.
- The communication between the various components of the prototype was implemented asynchronously, meaning that one component sends a task to another without interrupting its own work to wait for a response. For asynchronous data exchange, a database was used where one component stores a query in a designated table and another component appends its response after the task is completed. 

The challenges and activities related to the development of artificial intelligence were as follows:
- Selection of the clambering production process as the project focus. 
- Choosing a back-to-front approach for problem analysis. Process generation begins from a completed order, and while generating the process, we attempt to trace back to the beginning of the production process – down to the empty clamp assemblies.
- Identification and understanding of clamp assembly/preprocessing as a bottleneck in the production process through interviews. 
- Adjustment and validation of a brute-force algorithm that guarantees finding the optimal (i.e., most cost-effective) clamp assembly solution and serves as the baseline for verifying AI algorithms. The brute-force algorithm is based on applying recursive elementary operations to the input sheets to produce printable output clamps. 
- Realization of the cost function of bow assembly/pretreatment to evaluate the goodness of the solution.
- Optimizing the performance of the Brute Force algorithm to enable practical use.
- Implementation of two artificial intelligence algorithms:
  - Simulated Annealing
  - Monte Carlo Tree Search. This algorithm was not originally mentioned, but during the work it turned out that it fits well with the recursive bow assembly approach.
- Verification of these AI algorithms based on the price function compared to a brute force algorithm. The gain in speed is astronomical for larger issues, the loss in price is acceptable.
- Tuning of artificial intelligence algorithms.
- Comparison of artificial intelligence algorithms. MCTS has a slight advantage.
- Evaluation of the expansion possibilities of artificial intelligence algorithms. They are stronger on the MCTS algorithm, which can be extended with various pre-trained machine learning models to evaluate the goodness of the solution branch a’la AlphaZero.

### Data Sources
*Please describe which data was used for the technological solution.*  
- Data from the company's operational data database about historical orders and the operations performed to fulfill them. Based on this data, it can be checked whether the prototype being created would produce the same result for existing orders as a human expert would have achieved for existing orders.
- Information about the machines used by the company. Some of these data were also in the company's operational data database, but it turned out to be necessary to transform these data structures and collect additional data.
- Data on the papers used for printing and their properties (including price). This data also came from the company's operational data database.
- Examples of optimal manufacturing process models from industry experts for training and test data. 
- The rule for evaluating the optimality of the production process model.

### AI Technologies
*Please describe and justify the use of selected AI technologies.*
- We are dealing with an optimization problem where we are trying to minimize the cost of the process. A Brute Force algorithm is too slow, so heuristic optimization algorithms must be used. Optimized solutions are sets of bows assembled from input sheets. Elementary operations are used for assembly: 
  - Merging leaves into one bow.
  - Making multiple copies of the same page, resulting in a larger bow.
  - Merge the flipped version of the page next to the page. The front and back sides of the result are then the same.  This saves the printed circuit boards.
     There are both horizontal and vertical variants of these operations, and this gives a total of six elementary operations.
- Simulated annealing (SA) is a classic optimization algorithm and is recommended as a default solution to optimization problems by sources such as Algorithm Design Manual, S. Skiena. The algorithm is based on the iterative modification of the original random solution, where at the beginning of the process, transitions to solutions with a worse estimate are also likely (exploration of the solution space, avoiding getting stuck in the local optimum), but at the end of the process, such transitions are very unlikely (tuning the solution). Hence the analogy with the controlled lowering of the temperature during steel annealing.
- Monte Carlo Tree Search (MCTS) is a heuristic optimization algorithm that searches the solution tree for the most optimal solutions. MCTS is used for playing board games (chess, go) and, due to its tree-based approach, is well suited for the analysis of the solution tree generated by the elementary operations of bow assembly. MCTS is extensible with various pre-trained machine learning models (neural networks) that optimize the search. For example, the AlphaZero algorithm using pre-trained deep neural networks is extremely successful at playing chess and go. There are four main steps in a simple algorithm:
  - The choice of a half-baked solution with still unexplored possibilities for further development.
  - Choosing one such testing for further exploration.
  - Refining and evaluating that testing as the final solution (using Monte Carlo simulation).
  - Back-comparison and completion of tree nodes with new information.

The MCTS method has been adapted based on the special features of the bow assembly as follows:
  - In the tree structure, the sub-arches generated from the given arch and their sub-arches, i.e. 2 layers of sub-arches, are added as sub-branches of each leaf/arch. In this way, it was possible to make the structure of the tree as flat as possible, so that the algorithm goes through a wider number of solutions.
  - Tree branches that have already been searched to the end are excluded from the further selection, which helps to expand the search space and avoid situations where the algorithm "gets stuck" in the searched branch, because the best solution has come from there. 
MCTS helps to limit the amount of calculated bows, but the mentioned steps to expand this amount were still necessary. Bows generated in the upper layer of the tree were mostly more expensive and very similar in price compared to bows generated in the lower layers of the tree. Choosing the most favorable path in the upper layer of the tree was therefore a challenge for the MCTS method. Making the tree as flat as possible and excluding branches that were already searched to the end helped to ensure that the result found was as close as possible to the globally best price.

### Technological Results
*Please describe the results of testing and validating the technological solution.*

-	A more detailed comparison of the three post-processing solutions (print bow generation and price calculation) produced the results below. Let's call these solutions Brute Force, which generates and calculates all possible variations of the bows, and AI-centric Monte Carlo Tree Search (MCTS) and Simulated Annealing (SA), where the search space is optimized. 
- The Brute Force solution gives the best result when the input is small (up to 6 input pages), because it always finds the most favorable solution (Figure 1, number of input pages up to 6). For larger input, the model becomes unreasonably slow.
- An important advantage of MCTS and SA is their speed. Both models may or may not always find the most favorable global solution. However, the tests below show that the difference from the global minimum may not be large.
- In the SA algorithm, the degree of randomness is higher, i.e. to find the most favorable solution, it would be reasonable to execute the algorithm several times and then choose the most favorable solution.





Comparison of three algorithms for the following sets of input pages (run 10000, color 1):
1)	105x148
2)	302x216; 302x216; 302x216;302x216
3)	105x148; 74x105
4)	148x210;148x210; 148x210;148x210
5)	302x216; 150x216; 302x432; 150x432
6)	302x216; 302x216; 302x216; 302x216, 302x216; 302x216
7)	74x105; 74x105; 74x105; 74x105
8)	210x297; 148x210; 297x420; 594x420; 105x148
9)	148x210; 148x210; 148x210; 148x210; 148x210; 148x*210
10)	74x105; 210x297; 210x297; 210x297; 210x297
11)	105x148; 105x148; 105x148; 297x420; 297x420; 297x420
12)	302x216, 150x216, 302x432, 150x432, 150x108

![image](https://github.com/user-attachments/assets/930c66fa-4562-4809-862a-5241429e01d1)

Figure 1.

If the first six variations of the input page sets, where there are fewer input pages or the page sizes are larger, all 3 algorithms are calculated quite quickly. The differences are large from the seventh set of input sheets, where 1) there are more sheets in the set and 2) they are smaller in size or 3) they are of different sizes. For sets of input sheets 7 - 12, MCTS and SA take a maximum of twenty seconds, while the Brute Force model takes up to two hours to find a solution (Figure 1).

The speed of AI-based algorithms comes from the fact that they do not have to calculate the entire set of solutions to find the most optimal solution. Figure 2 shows the range of input bow placement variations computed by the Brute Force model and compares it to the set of solutions computed by the MCTS and SA models. If the input is only one sheet measuring 105*148 mm, it is possible to create 74 bow layout variations. If there are 5 input pages and they are all different sizes, the number of possible variations is 9.4 million. Figure 2 helps explain why the Brute Force algorithm becomes slow after the sixth input - the number of variations it calculates increases exponentially the more input pages there are.

  ![image](https://github.com/user-attachments/assets/e72b23be-dd53-49cc-be65-6223786e6161)

  Figure 2.

Compared to the most favourable prices found, the prices found by both MCTS and SA remained within the 5% margin of error, that is, the most favourable price found was the same as the price of the Brute Force solution or did not differ from it by more than 5% (Figure 3).

  ![image](https://github.com/user-attachments/assets/21820b82-de12-4d16-858b-5f1f66c9d331)

 Figure 3.

Testing the price differences separately in a comparison of the three models for 50 different combinations of input pages, where there was no more than a maximum of 3 input pages, it turned out that both MCTS and SA reached the same solution as the Brute Force model (or stayed within the 5% error rate) 96 % case. For MCTS, all prices obtained were within 5% error. In the case of SA, there were 2 cases out of 50 where the price difference was over 5%. Comparing the price averages, both AI-based algorithms were within 5% error.

The comparison between the MCTS and SA models for a set of six input pages gave a slight advantage to the MCTS model, which found a slightly better solution (marked in green in Figure 4). In this case, randomness has also been introduced into the MCTS model, and for each set of input sheets, both models were executed 5 times, tabulating the minimum and maximum prices obtained. The default column refers to the situation where the MCTS model was run without the randomness component.

Amounts of input sheets (run 10,000, color 1):
1) 210x297, 148x210, 297x420, 594x420, 105x148, 74x105
2) 210x297, 148x210, 105x148, 74x105, 52x74, 37x52
3) 302x216, 150x216, 302x432, 150x432, 150x108, 216x108
4) 302x216, 150x216, 148x210, 302x216, 150x216, 148x210
5) 52x74, 74x105, 37x52, 52x74, 74x105, 37x52
6) 302x216, 302x548, 74x105, 148x210, 105x148, 150x108

![image](https://github.com/user-attachments/assets/acf6d434-2c2e-4d3f-8ecf-c94be6520c29)

Figure 4.

The last three columns in Figure 4 highlight the price differences between the minimum-maximum price found, respectively, and in the case of MCTS, also between the minimum and default price. In the case of the MCTS algorithm, it can be seen that the minimum price found with the randomness component did not differ by more than ~5% from the price without the randomness component, and in three cases the price found by default is equal to the lowest price found based on randomness. The given figure also shows that when filling out the SA model, the difference between the minimum and maximum price can be quite large, which is why it is necessary to fill in the model repeatedly to find the most favourable solution.

### Technical Architecture
*Please describe the technical architecture (e.g, presented graphically, where the technical solution integration with the existing system can also be seen).*

Figure 5 of the architecture of the technical solution. Data tables are marked in blue, software components in red, data objects (inputs/outputs) in yellow.




![image](https://github.com/user-attachments/assets/8aa73f17-4562-49ae-bb39-6ec0d4eeca3e)

Figure 5.

### User Interface 
*Please describe the details about the user interface(i.e, how does the client 'see' the technical result, whether a separate user interface was developed, command line script was developed, was it validated as an experiment, can the results be seen in ERP or are they integrated into work process)*

Aktaprint sees the user interface of the made prototype as in the figure. The user interface displays the parameters of the customer order to be entered, the parameters of the company's machines; generated order workflows, workflow tasks and costs (Figure 6).

![image](https://github.com/user-attachments/assets/7e0d4b14-0a8b-45d1-8996-a3abc1d091a4)

Figure 6.

### Future Potential of the Technical Solution
*Please describe the potential areas for future use of the technical solution.*
- The solution can most likely be used in the production optimization and planning software of companies with a production schedule and production structure similar to a printing company, offering "custom made" solutions,
- The artificial intelligence solution has application potential in other production areas, where optimization is important, the number of possible solutions is large, and the solution space can be represented as a tree.

### Lessons Learned
*Please describe the lessons learned (i.e. assessment whether the technological solution actually solved the initial challenge).*

Lessons learned about data and databases: 
- Decisions—and the software outcomes—must be based on data. To make good decisions (for example, selecting the best order fulfillment method), high-quality data must be used. Unfortunately, the quality of data in existing databases may not be as good as it could be, so when planning software projects, it is necessary to account for the need to continuously improve data quality so that the data can be effectively utilized by the software being created.

- The creators of new registry-based systems should start from the assumption that the managed data will eventually be used in decision-making processes; therefore, ensuring data quality must be addressed throughout the entire creation process (just as security, performance, legality, and ethical issues must be handled throughout the entire process), because preventing problems is much more cost-effective than solving them afterward.

- A technical lesson is that in the popular database system MySQL, foreign key constraints were historically not enforced. Although this capability was added later, in many legacy MySQL databases these keys remain undefined. This not only poses a risk to data quality but also makes it more difficult for new parties to understand the data, as the database does not explicitly present information about how data objects are related. This information is not electronically available from the system but resides in the minds of the database creators (which is acceptable as long as they are available for inquiries). 

- Lack of software (including database) documentation becomes problematic when the software must be presented to someone who will then take over its maintenance or further refinement. 

Lessons learned about artificial intelligence-based solution: 
- The artificial intelligence-based solution is suitable for optimizing the bow assembly process. Both simulated annealing and Monte Carlo tree search algorithms give good results. 

- The complexity of manufacturing and business processes makes building a general AI solution labour-intensive. Finding bottlenecks in the process with a complex search space and optimizing their performance with heuristic AI algorithms seems a more realistic alternative. 

- The existence of an optimisable price function enables verification, which, unlike the training and test data of classical supervised learning, uses the guaranteed optimal solutions found by the brute force algorithm as a reference base.

# Custom agreement with the AIRE team
*If you have a unique project or specific requirements that don't fit neatly into the Docker file or description template options, we welcome custom agreements with our AIRE team. This option allows flexibility in collaborating with us to ensure your project's needs are met effectively.*

*To explore this option, please contact our demonstration projects service manager via katre.eljas@taltech.ee with the subject line "Demonstration Project Custom Agreement Request - [Your Project Name]." In your email, briefly describe your project and your specific documentation or collaboration needs. Our team will promptly respond to initiate a conversation about tailoring a solution that aligns with your project goals.*
