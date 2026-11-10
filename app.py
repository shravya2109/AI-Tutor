from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json, random, os

app = Flask(__name__)
app.secret_key = "aitutor_secret_2025"

USERS = {}

QUIZZES = {
    "Python Programming": [
        {"question":"What is the output of print(type([]))?","options":["<class 'tuple'>","<class 'list'>","<class 'dict'>","<class 'set'>"],"answer":1,"explanation":"[] creates an empty list, so type([]) returns <class 'list'>."},
        {"question":"Which keyword defines a function in Python?","options":["function","fun","def","define"],"answer":2,"explanation":"'def' is Python's keyword for defining functions."},
        {"question":"What does len('hello') return?","options":["4","6","5","Error"],"answer":2,"explanation":"'hello' has 5 characters, so len() returns 5."},
        {"question":"Which data type is mutable in Python?","options":["tuple","string","int","list"],"answer":3,"explanation":"Lists are mutable — you can add, change, or remove elements."},
        {"question":"How do you create an empty dictionary?","options":["d = []","d = {}","d = ()","d = set()"],"answer":1,"explanation":"Curly braces {} create an empty dictionary."},
        {"question":"What does range(3) produce?","options":["[1,2,3]","[0,1,2,3]","[0,1,2]","[1,2]"],"answer":2,"explanation":"range(3) generates 0, 1, 2 — up to but not including 3."},
        {"question":"Which method adds an element to end of a list?","options":["list.add()","list.push()","list.append()","list.extend()"],"answer":2,"explanation":"list.append(item) adds a single item to the end of a list."},
        {"question":"What is the result of 10 // 3?","options":["3.33","3","4","1"],"answer":1,"explanation":"// is floor division — 10 // 3 = 3."},
        {"question":"What does *args allow in a function?","options":["Keyword arguments","Variable positional arguments","Default values","None of these"],"answer":1,"explanation":"*args collects any number of positional arguments into a tuple."},
        {"question":"Which statement handles exceptions in Python?","options":["catch","handle","try/except","error/fix"],"answer":2,"explanation":"try/except is Python's exception handling mechanism."},
        {"question":"What is a lambda function?","options":["A named function","A class method","An anonymous one-line function","A built-in function"],"answer":2,"explanation":"Lambda creates small anonymous functions: lambda x: x*2."},
        {"question":"What does enumerate() return?","options":["A list","Index-value pairs","Only indices","Only values"],"answer":1,"explanation":"enumerate() returns (index, value) pairs for each element."},
    ],
    "Machine Learning": [
        {"question":"Which algorithm is used for binary classification?","options":["Linear Regression","K-Means","Logistic Regression","PCA"],"answer":2,"explanation":"Logistic Regression predicts class probabilities for binary classification."},
        {"question":"What does overfitting mean?","options":["Model underperforms on training","Model memorizes training data but fails on new data","Model is too simple","Model trains too fast"],"answer":1,"explanation":"Overfitting: model learns noise in training data, performs poorly on unseen examples."},
        {"question":"What is the purpose of train/test split?","options":["Speed up training","Reduce dataset size","Evaluate model on unseen data","Improve training accuracy"],"answer":2,"explanation":"Train/test split lets us evaluate generalization to unseen data."},
        {"question":"Which metric suits imbalanced classification?","options":["Accuracy","F1 Score","MSE","R-squared"],"answer":1,"explanation":"F1 Score balances precision and recall, reliable for imbalanced datasets."},
        {"question":"What does PCA stand for?","options":["Predictive Cluster Analysis","Principal Component Analysis","Probabilistic Classification Algorithm","Parametric Correction Approach"],"answer":1,"explanation":"PCA reduces dimensionality by finding directions of maximum variance."},
        {"question":"What is gradient descent?","options":["A data cleaning method","An optimization algorithm to minimize loss","A classification algorithm","A feature selection technique"],"answer":1,"explanation":"Gradient descent iteratively adjusts weights to minimize the loss function."},
        {"question":"What is the bias-variance tradeoff?","options":["Speed vs accuracy","Underfitting vs overfitting balance","Training vs test size","Precision vs recall"],"answer":1,"explanation":"Bias = underfitting error; Variance = overfitting sensitivity. We balance both."},
        {"question":"Which library is most used for ML in Python?","options":["TensorFlow","PyTorch","scikit-learn","Keras"],"answer":2,"explanation":"scikit-learn provides simple, consistent ML tools and is the most widely used library."},
        {"question":"What does cross-validation do?","options":["Splits data randomly","Tests model on multiple folds for reliable evaluation","Cleans data","Selects features"],"answer":1,"explanation":"Cross-validation evaluates models on multiple splits to reduce evaluation variance."},
        {"question":"What is a decision tree?","options":["A graph algorithm","A flowchart-like model that makes decisions based on features","A neural network type","A clustering method"],"answer":1,"explanation":"Decision trees split data at feature thresholds to make predictions."},
        {"question":"What is regularization in ML?","options":["Normalization of features","A penalty on model complexity to prevent overfitting","Increasing model size","A type of activation function"],"answer":1,"explanation":"Regularization (L1/L2) adds penalty terms to reduce overfitting."},
        {"question":"What does feature engineering mean?","options":["Building hardware features","Creating/transforming input variables to improve model performance","Selecting the best model","Deploying a model"],"answer":1,"explanation":"Feature engineering transforms raw data into informative inputs for ML models."},
    ],
    "Data Science": [
        {"question":"Which Pandas method shows basic statistics?","options":["df.info()","df.head()","df.describe()","df.shape"],"answer":2,"explanation":"df.describe() shows count, mean, std, min, max, quartiles for numeric columns."},
        {"question":"What does A/B testing measure?","options":["Data quality","Statistical significance between two variants","Model accuracy","Query speed"],"answer":1,"explanation":"A/B testing compares two variants to determine statistical significance."},
        {"question":"Which chart best shows distribution of a variable?","options":["Pie chart","Line chart","Histogram","Scatter plot"],"answer":2,"explanation":"Histograms show frequency distribution across value ranges."},
        {"question":"What is the purpose of data normalization?","options":["Remove missing values","Scale features to a common range","Visualize data","Split datasets"],"answer":1,"explanation":"Normalization scales features to a common range for fair model training."},
        {"question":"What does ETL stand for?","options":["Extract, Train, Load","Extract, Transform, Load","Evaluate, Test, Learn","Export, Transform, Label"],"answer":1,"explanation":"ETL = Extract, Transform, Load — the data pipeline process."},
        {"question":"What is a p-value?","options":["Model accuracy score","Probability of observing results if null hypothesis is true","Feature importance score","Variance measure"],"answer":1,"explanation":"p-value measures how likely the observed result is under the null hypothesis."},
        {"question":"Which SQL clause filters grouped data?","options":["WHERE","HAVING","GROUP BY","ORDER BY"],"answer":1,"explanation":"HAVING filters results after GROUP BY; WHERE filters before grouping."},
        {"question":"What is an outlier?","options":["A missing value","A data point significantly different from others","A duplicate record","A categorical variable"],"answer":1,"explanation":"Outliers are extreme values that deviate significantly from the bulk of data."},
        {"question":"What is the median?","options":["Most frequent value","Sum divided by count","Middle value when sorted","Square root of variance"],"answer":2,"explanation":"The median is the middle value in a sorted dataset, robust to outliers."},
        {"question":"What does data wrangling mean?","options":["Visualizing data","Cleaning and transforming raw data into usable format","Building ML models","Querying databases"],"answer":1,"explanation":"Data wrangling cleans, reshapes, and transforms messy data for analysis."},
        {"question":"What is a correlation coefficient?","options":["A measure of dataset size","A value between -1 and 1 indicating linear relationship strength","Model accuracy","Feature count"],"answer":1,"explanation":"Correlation coefficient (-1 to 1) indicates strength/direction of linear relationships."},
    ],
    "Web Development": [
        {"question":"Which HTML tag creates a hyperlink?","options":["<link>","<href>","<a>","<url>"],"answer":2,"explanation":"The <a> (anchor) tag with href attribute creates clickable hyperlinks."},
        {"question":"Which CSS property controls space outside an element?","options":["padding","border","margin","spacing"],"answer":2,"explanation":"margin is space outside the border; padding is space inside the border."},
        {"question":"What does DOM stand for?","options":["Document Object Model","Data Object Management","Dynamic Output Module","Document Output Method"],"answer":0,"explanation":"DOM (Document Object Model) represents HTML as a tree JavaScript can manipulate."},
        {"question":"What does CSS Flexbox primarily help with?","options":["Animations","1D layout of items in a row or column","Database queries","Server routing"],"answer":1,"explanation":"Flexbox provides powerful 1D layout control for rows or columns."},
        {"question":"What is the purpose of async/await in JavaScript?","options":["Define classes","Handle asynchronous operations cleanly","Style elements","Create loops"],"answer":1,"explanation":"async/await makes asynchronous code like API calls readable and easy to reason about."},
        {"question":"What does HTTP stand for?","options":["HyperText Transfer Protocol","High Tech Text Processing","Hyperlink Transfer Process","HyperText Terminal Protocol"],"answer":0,"explanation":"HTTP (HyperText Transfer Protocol) is the foundation of web data communication."},
        {"question":"What is a REST API?","options":["A database","An architectural style using HTTP","A JavaScript framework","A CSS library"],"answer":1,"explanation":"REST API uses HTTP methods (GET, POST, PUT, DELETE) to interact with resources."},
        {"question":"What does localStorage store?","options":["Server-side data","Key-value pairs in the browser persistently","Session cookies","Database records"],"answer":1,"explanation":"localStorage stores key-value pairs in the browser that persist across reloads."},
        {"question":"What is React's Virtual DOM?","options":["A real browser DOM","A lightweight JS representation for efficient updates","A CSS framework","A database layer"],"answer":1,"explanation":"React's Virtual DOM minimizes real DOM manipulations by diffing changes efficiently."},
        {"question":"What is CORS?","options":["A CSS property","Cross-Origin Resource Sharing — controls cross-domain requests","A JavaScript loop","A web server"],"answer":1,"explanation":"CORS is a browser security mechanism controlling which origins can access resources."},
        {"question":"What is the box model in CSS?","options":["A 3D rendering technique","Content, padding, border, and margin around elements","A JavaScript pattern","A layout grid"],"answer":1,"explanation":"The CSS box model describes content surrounded by padding, border, and margin."},
    ],
    "Artificial Intelligence": [
        {"question":"What is a neural network inspired by?","options":["Computer circuits","The human brain's neuron structure","Mathematical matrices only","Statistical regression"],"answer":1,"explanation":"Neural networks mimic biological neurons using interconnected nodes."},
        {"question":"What does NLP stand for?","options":["Numerical Learning Protocol","Natural Language Processing","Neural Logic Programming","Network Layer Protocol"],"answer":1,"explanation":"NLP (Natural Language Processing) enables computers to understand human language."},
        {"question":"Which company released the Transformer architecture paper?","options":["OpenAI","Meta","Google","Microsoft"],"answer":2,"explanation":"Google released 'Attention Is All You Need' in 2017, introducing Transformers."},
        {"question":"What is reinforcement learning?","options":["Learning from labeled data","Learning by receiving rewards/penalties from an environment","Unsupervised clustering","Transfer learning"],"answer":1,"explanation":"RL agents learn by interacting with environments and receiving reward signals."},
        {"question":"What is a GAN?","options":["Global Attention Network","Generative Adversarial Network","Graph Attention Node","General AI Network"],"answer":1,"explanation":"GANs have a Generator and Discriminator competing to improve fake data generation."},
        {"question":"What is transfer learning?","options":["Moving data between servers","Reusing a pre-trained model for a new related task","Training from scratch","Data augmentation"],"answer":1,"explanation":"Transfer learning leverages knowledge from one task to improve learning on another."},
        {"question":"What does CNN stand for in deep learning?","options":["Convolutional Neural Network","Centralized Neural Node","Cyclic Network Node","Computed Neuron Network"],"answer":0,"explanation":"CNN (Convolutional Neural Network) is designed for processing grid-like data like images."},
        {"question":"What is the attention mechanism in transformers?","options":["A memory module","Weights determining focus on each input token","A loss function","A regularization technique"],"answer":1,"explanation":"Attention allows models to weigh importance of each token relative to others in context."},
        {"question":"What is a hyperparameter?","options":["A training data feature","A configuration set before training (e.g., learning rate)","A model output","A type of activation"],"answer":1,"explanation":"Hyperparameters (learning rate, epochs) are set before training to control the process."},
        {"question":"What is prompt engineering?","options":["Building hardware prompts","Crafting input text to guide LLM outputs effectively","Training language models","A data preprocessing step"],"answer":1,"explanation":"Prompt engineering designs effective inputs to get desired outputs from LLMs."},
        {"question":"What is an embedding in NLP?","options":["A compression algorithm","A dense vector representation of words/tokens","A tokenization method","A data format"],"answer":1,"explanation":"Embeddings map words/tokens to dense numeric vectors capturing semantic meaning."},
    ],
    "Mathematics": [
        {"question":"What is the derivative of sin(x)?","options":["cos(x)","-cos(x)","tan(x)","-sin(x)"],"answer":0,"explanation":"The derivative of sin(x) is cos(x)."},
        {"question":"What is the value of Euler's number e?","options":["2.718","3.141","1.618","2.301"],"answer":0,"explanation":"e ≈ 2.71828..., the base of the natural logarithm."},
        {"question":"What is the quadratic formula?","options":["x = -b ± sqrt(b2-4ac) / 2a","x = b ± sqrt(b2+4ac) / 2a","x = -b / 2a","x = -(b+c)/a"],"answer":0,"explanation":"Quadratic formula: x = (-b ± √(b²-4ac)) / 2a."},
        {"question":"What does a matrix determinant of 0 indicate?","options":["Identity matrix","Matrix is invertible","Matrix is singular (not invertible)","Matrix is diagonal"],"answer":2,"explanation":"A determinant of 0 means the matrix is singular — it has no inverse."},
        {"question":"What is a prime number?","options":["Divisible by 2","Divisible only by 1 and itself","An even number > 2","A perfect square"],"answer":1,"explanation":"A prime is only divisible by 1 and itself (e.g., 2, 3, 5, 7, 11)."},
        {"question":"What is the integral of 1/x dx?","options":["x","ln|x| + C","1/x2 + C","ex + C"],"answer":1,"explanation":"The integral of 1/x is ln|x| + C."},
        {"question":"What is the Pythagorean theorem?","options":["a+b=c","a2+b2=c2","a2-b2=c2","2a+b=c2"],"answer":1,"explanation":"In a right triangle: a² + b² = c², where c is the hypotenuse."},
        {"question":"What is the dot product of two perpendicular vectors?","options":["1","-1","0","Undefined"],"answer":2,"explanation":"The dot product of two perpendicular (orthogonal) vectors is 0."},
        {"question":"What is the probability of flipping heads twice in a row?","options":["1/2","1/4","1/3","3/4"],"answer":1,"explanation":"P(HH) = 1/2 × 1/2 = 1/4, since each flip is independent."},
        {"question":"What is the sum of angles in a triangle?","options":["90°","180°","270°","360°"],"answer":1,"explanation":"Interior angles of any triangle sum to 180°."},
    ],
    "Physics": [
        {"question":"What is Newton's second law?","options":["F = ma","E = mc2","v = u + at","F = G(m1m2/r2)"],"answer":0,"explanation":"Newton's 2nd law: Force = mass × acceleration (F = ma)."},
        {"question":"What is the speed of light in a vacuum?","options":["3x106 m/s","3x108 m/s","3x1010 m/s","3x104 m/s"],"answer":1,"explanation":"Speed of light c ≈ 3×10⁸ m/s."},
        {"question":"What does E=mc2 represent?","options":["Kinetic energy formula","Mass-energy equivalence","Gravitational potential energy","Ohm's law"],"answer":1,"explanation":"E=mc² shows mass and energy are equivalent (Einstein)."},
        {"question":"What is Ohm's Law?","options":["V = IR","P = IV","F = ma","E = hf"],"answer":0,"explanation":"Ohm's Law: Voltage = Current × Resistance (V = IR)."},
        {"question":"What type of wave is sound?","options":["Transverse wave","Longitudinal wave","Electromagnetic wave","Standing wave"],"answer":1,"explanation":"Sound is a longitudinal wave — particles vibrate parallel to wave travel."},
        {"question":"What is the unit of electric current?","options":["Volt","Ohm","Ampere","Watt"],"answer":2,"explanation":"Electric current is measured in Amperes (A)."},
        {"question":"What is entropy in thermodynamics?","options":["Heat energy","A measure of disorder/randomness in a system","Temperature change","Pressure times volume"],"answer":1,"explanation":"Entropy measures the degree of disorder or randomness in a thermodynamic system."},
        {"question":"What is the phenomenon of light bending around an object?","options":["Reflection","Refraction","Diffraction","Dispersion"],"answer":2,"explanation":"Diffraction is the bending of waves around obstacles or through openings."},
        {"question":"What is the half-life of a radioactive substance?","options":["Time to fully decay","Time for half the atoms to decay","Maximum energy release","Initial activity level"],"answer":1,"explanation":"Half-life is the time for half of a radioactive sample to undergo decay."},
        {"question":"What force keeps planets in orbit?","options":["Electromagnetic force","Nuclear force","Gravitational force","Centrifugal force"],"answer":2,"explanation":"Gravity provides the centripetal force keeping planets in orbit."},
    ],
    "Chemistry": [
        {"question":"What is the atomic number of Carbon?","options":["6","12","14","8"],"answer":0,"explanation":"Carbon has atomic number 6 — it has 6 protons."},
        {"question":"What is the pH of pure water?","options":["5","6","7","8"],"answer":2,"explanation":"Pure water has a neutral pH of 7 at 25°C."},
        {"question":"What type of bond involves sharing electrons?","options":["Ionic bond","Covalent bond","Metallic bond","Hydrogen bond"],"answer":1,"explanation":"Covalent bonds involve sharing electron pairs between atoms."},
        {"question":"What is the chemical formula for water?","options":["H2O2","HO","H2O","H3O"],"answer":2,"explanation":"Water is H₂O — two hydrogen atoms bonded to one oxygen atom."},
        {"question":"What is the most abundant element in Earth's crust?","options":["Silicon","Iron","Oxygen","Aluminum"],"answer":2,"explanation":"Oxygen makes up about 46% of Earth's crust by mass."},
        {"question":"What does an acid do in water?","options":["Releases OH- ions","Releases H+ ions","Releases neutral molecules","Absorbs electrons"],"answer":1,"explanation":"Acids donate protons (H+ ions) when dissolved in water."},
        {"question":"What is the periodic table organized by?","options":["Atomic mass","Alphabetical order","Atomic number","Electron configuration"],"answer":2,"explanation":"The modern periodic table is organized by increasing atomic number."},
        {"question":"What is an isotope?","options":["Same element, different electron count","Same element, different neutron count","Different element, same mass","A radioactive particle"],"answer":1,"explanation":"Isotopes are atoms of the same element with different numbers of neutrons."},
        {"question":"What is Avogadro's number?","options":["6.022 x 1023","3.14 x 1023","1.38 x 1023","9.11 x 1023"],"answer":0,"explanation":"Avogadro's number ≈ 6.022×10²³ particles per mole."},
        {"question":"What is a catalyst?","options":["A reactant consumed in the reaction","A substance that speeds up reaction without being consumed","A product of reaction","An inhibitor"],"answer":1,"explanation":"A catalyst speeds up reactions without being permanently changed."},
    ],
    "English Literature": [
        {"question":"Who wrote Romeo and Juliet?","options":["Charles Dickens","William Shakespeare","Jane Austen","John Keats"],"answer":1,"explanation":"Romeo and Juliet was written by William Shakespeare, around 1594-1596."},
        {"question":"Which literary device uses like or as for comparison?","options":["Metaphor","Simile","Hyperbole","Personification"],"answer":1,"explanation":"A simile compares two things using 'like' or 'as' (e.g., brave as a lion)."},
        {"question":"What is the protagonist?","options":["The villain","The main character the story revolves around","The narrator","A minor character"],"answer":1,"explanation":"The protagonist is the main character — the central figure in the story's conflict."},
        {"question":"What is iambic pentameter?","options":["A type of rhyme","A meter with 5 iambs (10 syllables) per line","A stanza form","A narrative technique"],"answer":1,"explanation":"Iambic pentameter has 5 iambs (da-DUM) per line — 10 syllables. Used by Shakespeare."},
        {"question":"What is a haiku?","options":["A 14-line poem","A Japanese poem with 5-7-5 syllable structure","A narrative poem","A free verse poem"],"answer":1,"explanation":"A haiku has 3 lines: 5, 7, 5 syllables — a Japanese poetic form."},
        {"question":"What is dramatic irony?","options":["A funny scene","When audience knows something characters don't","A character's internal conflict","A plot twist"],"answer":1,"explanation":"Dramatic irony occurs when the audience has knowledge the characters lack."},
        {"question":"Who wrote 1984?","options":["Aldous Huxley","Ray Bradbury","George Orwell","H.G. Wells"],"answer":2,"explanation":"1984 was written by George Orwell, published in 1949."},
        {"question":"What is an allegory?","options":["A long poem","A story with symbolic meaning representing deeper ideas","A type of metaphor","An exaggerated statement"],"answer":1,"explanation":"An allegory is a narrative where characters/events symbolize abstract ideas."},
        {"question":"What does omniscient narrator mean?","options":["First-person narrator","A narrator who knows all characters' thoughts and events","An unreliable narrator","A character who is also the author"],"answer":1,"explanation":"An omniscient narrator has complete knowledge of all characters' thoughts and events."},
        {"question":"What is the climax of a story?","options":["The opening","The point of highest tension and turning point","The resolution","The backstory"],"answer":1,"explanation":"The climax is the peak moment of tension — the story's turning point."},
    ],
    "History": [
        {"question":"In which year did World War II end?","options":["1943","1944","1945","1946"],"answer":2,"explanation":"WWII ended in 1945 — V-E Day (May 8) in Europe, V-J Day (Sept 2) in the Pacific."},
        {"question":"Who was the first President of the United States?","options":["John Adams","Thomas Jefferson","Benjamin Franklin","George Washington"],"answer":3,"explanation":"George Washington was inaugurated as the 1st U.S. President on April 30, 1789."},
        {"question":"The French Revolution began in which year?","options":["1776","1789","1804","1815"],"answer":1,"explanation":"The French Revolution began in 1789 with the storming of the Bastille."},
        {"question":"Who wrote the Communist Manifesto?","options":["Lenin and Stalin","Marx and Engels","Trotsky and Mao","Bakunin and Proudhon"],"answer":1,"explanation":"The Communist Manifesto was written by Karl Marx and Friedrich Engels in 1848."},
        {"question":"Which empire was the largest in history by land area?","options":["Roman Empire","British Empire","Mongol Empire","Ottoman Empire"],"answer":2,"explanation":"The Mongol Empire (13th-14th century) was the largest contiguous land empire."},
        {"question":"In what year did the Berlin Wall fall?","options":["1985","1987","1989","1991"],"answer":2,"explanation":"The Berlin Wall fell on November 9, 1989."},
        {"question":"Which ancient wonder was located in Alexandria?","options":["Colossus of Rhodes","Lighthouse of Alexandria","Hanging Gardens","Temple of Artemis"],"answer":1,"explanation":"The Lighthouse of Alexandria (Pharos) stood in Alexandria's harbour."},
        {"question":"What was the name of the first artificial satellite?","options":["Explorer 1","Luna 1","Sputnik 1","Vostok 1"],"answer":2,"explanation":"Sputnik 1, launched by the USSR on October 4, 1957, was the first artificial satellite."},
        {"question":"Who was the Egyptian queen associated with Julius Caesar?","options":["Nefertiti","Hatshepsut","Cleopatra","Isis"],"answer":2,"explanation":"Cleopatra VII formed alliances with Julius Caesar and Mark Antony."},
        {"question":"What triggered World War I?","options":["German invasion of Poland","Assassination of Archduke Franz Ferdinand","Russian Revolution","Treaty of Versailles"],"answer":1,"explanation":"Assassination of Archduke Franz Ferdinand in Sarajevo (1914) triggered WWI."},
    ],
    "Cybersecurity": [
        {"question":"What does SQL injection exploit?","options":["Network vulnerabilities","Unsanitized database queries via user input","Weak passwords","Buffer overflows"],"answer":1,"explanation":"SQL injection inserts malicious SQL code into queries via unvalidated user input."},
        {"question":"What is phishing?","options":["Network scanning","Deceiving users into revealing sensitive info via fake communications","A type of malware","Password cracking"],"answer":1,"explanation":"Phishing uses fraudulent emails/sites to trick users into revealing credentials."},
        {"question":"What does HTTPS provide over HTTP?","options":["Faster loading","Encrypted communication via TLS/SSL","Compression","Caching"],"answer":1,"explanation":"HTTPS encrypts data in transit using TLS/SSL."},
        {"question":"What is a firewall?","options":["An antivirus program","A network security system monitoring and filtering traffic","A VPN service","An encryption algorithm"],"answer":1,"explanation":"A firewall monitors and controls incoming/outgoing network traffic."},
        {"question":"What is two-factor authentication (2FA)?","options":["Two passwords","Security using two different verification methods","Double encryption","Biometric login only"],"answer":1,"explanation":"2FA requires two distinct verification factors for authentication."},
        {"question":"What does zero-day vulnerability mean?","options":["A vulnerability fixed immediately","An unknown vulnerability with no patch available yet","A vulnerability found on day zero","A low-severity bug"],"answer":1,"explanation":"Zero-day means the vulnerability is unknown to the vendor — zero days for a patch."},
        {"question":"What is a DDoS attack?","options":["Data theft via malware","Overwhelming a server with massive traffic","Man-in-the-middle attack","Password spraying"],"answer":1,"explanation":"DDoS floods a target with traffic from many sources, causing downtime."},
        {"question":"What is the purpose of hashing passwords?","options":["Compress data","Store passwords as irreversible strings for security","Encrypt data for transmission","Speed up authentication"],"answer":1,"explanation":"Hashing converts passwords to irreversible strings — safe even if DB is breached."},
        {"question":"What is a VPN?","options":["A type of firewall","Virtual Private Network — encrypts traffic and hides IP","An antivirus tool","A network scanner"],"answer":1,"explanation":"A VPN creates an encrypted tunnel for internet traffic, masking your IP."},
        {"question":"What does man-in-the-middle attack mean?","options":["Hacking a server directly","Intercepting communication between two parties","Brute forcing passwords","Social engineering"],"answer":1,"explanation":"MITM attacks secretly intercept and potentially alter communications between two parties."},
    ],
    "Cloud Computing": [
        {"question":"What does IaaS stand for?","options":["Internet as a Service","Infrastructure as a Service","Integration as a Service","Interface as a Service"],"answer":1,"explanation":"IaaS (Infrastructure as a Service) provides virtualized computing resources online."},
        {"question":"Which is a major cloud provider?","options":["Oracle DB","AWS (Amazon Web Services)","Git","Jenkins"],"answer":1,"explanation":"AWS (Amazon Web Services) is the world's leading cloud computing platform."},
        {"question":"What is containerization?","options":["Physical server management","Packaging apps with dependencies into isolated containers","Virtual machine technology","Data compression"],"answer":1,"explanation":"Containerization (e.g., Docker) packages apps with dependencies in portable containers."},
        {"question":"What does serverless mean in cloud computing?","options":["No servers exist","Developers deploy code without managing server infrastructure","Free cloud service","Offline computing"],"answer":1,"explanation":"Serverless lets developers run code without provisioning or managing servers."},
        {"question":"What is auto-scaling?","options":["Automatic code deployment","Automatically adjusting compute resources based on demand","Load balancing","Database scaling"],"answer":1,"explanation":"Auto-scaling automatically adjusts instances based on traffic to optimize cost/performance."},
        {"question":"What is a CDN?","options":["Central Data Node","Content Delivery Network — distributes content closer to users","Cloud Database Network","Continuous Deployment Node"],"answer":1,"explanation":"A CDN caches and serves content from servers geographically close to users."},
        {"question":"What is Kubernetes used for?","options":["Version control","Container orchestration and management","Database management","Network security"],"answer":1,"explanation":"Kubernetes automates deployment, scaling, and management of containerized applications."},
        {"question":"What is the difference between SaaS and PaaS?","options":["No difference","SaaS provides full apps; PaaS provides a platform to build apps","SaaS is for storage; PaaS is for compute","SaaS is open source; PaaS is proprietary"],"answer":1,"explanation":"SaaS = full software over internet (e.g., Gmail); PaaS = development platform (e.g., Heroku)."},
        {"question":"What does high availability mean in cloud?","options":["Fast internet connection","System designed to minimize downtime","High bandwidth","Expensive pricing tier"],"answer":1,"explanation":"High availability minimizes downtime through redundancy, failover, and load balancing."},
        {"question":"What is object storage?","options":["RAM management","Storage for unstructured data as objects with metadata (e.g., S3)","SQL database type","File compression method"],"answer":1,"explanation":"Object storage (like AWS S3) stores unstructured data as objects with IDs and metadata."},
    ],
}

LEARNING_PATHS = {
    "Python Programming": [
        {"step":1,"title":"Python Basics & Setup","desc":"Install Python & VS Code. Variables, data types, print, arithmetic.","duration":"1–2 hours"},
        {"step":2,"title":"Control Flow","desc":"if/elif/else, for/while loops, break, continue, nested logic.","duration":"2–3 hours"},
        {"step":3,"title":"Functions & Modules","desc":"Write reusable functions. Import and use standard library modules.","duration":"2–3 hours"},
        {"step":4,"title":"Data Structures","desc":"Lists, tuples, dicts, sets. List comprehensions and dict operations.","duration":"2–3 hours"},
        {"step":5,"title":"File I/O & Exceptions","desc":"Read/write files. Handle errors with try/except/finally.","duration":"2–3 hours"},
        {"step":6,"title":"Capstone Project","desc":"Build a complete CLI app — To-do manager, Quiz game, or Weather fetcher.","duration":"4–5 hours"},
    ],
    "Machine Learning": [
        {"step":1,"title":"Math & Python Foundations","desc":"Linear algebra, statistics, probability. NumPy, Pandas, Matplotlib.","duration":"3–4 hours"},
        {"step":2,"title":"Data Preprocessing","desc":"Clean data, handle missing values, encode categoricals, normalize features.","duration":"2–3 hours"},
        {"step":3,"title":"Supervised Learning","desc":"Train regression and classification models with scikit-learn.","duration":"4–5 hours"},
        {"step":4,"title":"Model Evaluation","desc":"Accuracy, precision, recall, F1-score, ROC-AUC. Cross-validation.","duration":"3–4 hours"},
        {"step":5,"title":"Unsupervised Learning","desc":"K-Means clustering, hierarchical clustering, PCA.","duration":"3–4 hours"},
        {"step":6,"title":"End-to-End ML Project","desc":"Complete pipeline: raw data to model deployment.","duration":"6–8 hours"},
    ],
    "Data Science": [
        {"step":1,"title":"Python & Pandas Basics","desc":"DataFrame operations, filtering, groupby, merge/join, cleaning.","duration":"3–4 hours"},
        {"step":2,"title":"Data Visualization","desc":"Charts with Matplotlib, Seaborn, and Plotly. Data storytelling.","duration":"2–3 hours"},
        {"step":3,"title":"Exploratory Data Analysis","desc":"Distributions, correlations, outlier detection, feature understanding.","duration":"2–3 hours"},
        {"step":4,"title":"Statistics for Data Science","desc":"Hypothesis testing, p-values, confidence intervals, A/B testing.","duration":"3–4 hours"},
        {"step":5,"title":"SQL & Databases","desc":"SQL queries, joins, subqueries, window functions.","duration":"3–4 hours"},
        {"step":6,"title":"Capstone Data Project","desc":"Data collection → cleaning → EDA → insights → report.","duration":"5–6 hours"},
    ],
    "Web Development": [
        {"step":1,"title":"HTML Fundamentals","desc":"HTML structure, semantic tags, forms, tables, links, images.","duration":"2–3 hours"},
        {"step":2,"title":"CSS Styling","desc":"Selectors, box model, flexbox, CSS Grid, responsive design.","duration":"3–4 hours"},
        {"step":3,"title":"JavaScript Basics","desc":"Variables, functions, DOM manipulation, events, fetch API.","duration":"4–5 hours"},
        {"step":4,"title":"React Framework","desc":"Components, props, state, hooks, React Router.","duration":"5–6 hours"},
        {"step":5,"title":"Backend with Node.js","desc":"REST APIs with Express.js, middleware, routing, MongoDB.","duration":"5–6 hours"},
        {"step":6,"title":"Full-Stack Project","desc":"Build and deploy a full-stack web app with auth and live database.","duration":"8–10 hours"},
    ],
    "Artificial Intelligence": [
        {"step":1,"title":"AI Foundations","desc":"AI vs ML vs DL. History, key concepts, current landscape.","duration":"2–3 hours"},
        {"step":2,"title":"Python for AI","desc":"NumPy, Pandas, Matplotlib. AI development environment setup.","duration":"3–4 hours"},
        {"step":3,"title":"Machine Learning Basics","desc":"Supervised, unsupervised, RL. Train your first ML model.","duration":"4–5 hours"},
        {"step":4,"title":"Deep Learning & Neural Networks","desc":"Perceptrons, backprop, CNNs, RNNs with TensorFlow/Keras.","duration":"5–6 hours"},
        {"step":5,"title":"NLP & Large Language Models","desc":"Transformers, BERT, GPT concepts, Hugging Face pipelines.","duration":"4–5 hours"},
        {"step":6,"title":"AI Capstone Project","desc":"Build an AI-powered app: chatbot, classifier, or recommender.","duration":"6–8 hours"},
    ],
    "Mathematics": [
        {"step":1,"title":"Algebra & Functions","desc":"Equations, inequalities, polynomials, and function types.","duration":"2–3 hours"},
        {"step":2,"title":"Calculus Fundamentals","desc":"Limits, derivatives, differentiation rules and applications.","duration":"3–4 hours"},
        {"step":3,"title":"Integration","desc":"Definite and indefinite integrals, substitution, integration by parts.","duration":"3–4 hours"},
        {"step":4,"title":"Linear Algebra","desc":"Vectors, matrices, determinants, eigenvalues, transformations.","duration":"4–5 hours"},
        {"step":5,"title":"Probability & Statistics","desc":"Probability rules, distributions, hypothesis testing, regression.","duration":"3–4 hours"},
        {"step":6,"title":"Applied Math Project","desc":"Use math to solve a real problem in finance, physics, or data science.","duration":"3–4 hours"},
    ],
    "Physics": [
        {"step":1,"title":"Mechanics","desc":"Kinematics, Newton's laws, energy, momentum, rotational motion.","duration":"4–5 hours"},
        {"step":2,"title":"Thermodynamics","desc":"Heat, temperature, laws of thermodynamics, entropy.","duration":"3–4 hours"},
        {"step":3,"title":"Waves & Optics","desc":"Wave properties, sound, light, reflection, refraction, diffraction.","duration":"3–4 hours"},
        {"step":4,"title":"Electricity & Magnetism","desc":"Circuits, Ohm's law, capacitors, electromagnetic induction.","duration":"4–5 hours"},
        {"step":5,"title":"Modern Physics","desc":"Relativity, quantum mechanics, atomic structure, nuclear physics.","duration":"4–5 hours"},
        {"step":6,"title":"Physics Problem Set","desc":"Solve 20 multi-topic problems covering all areas studied.","duration":"3–4 hours"},
    ],
    "Chemistry": [
        {"step":1,"title":"Atomic Structure","desc":"Protons, neutrons, electrons, orbitals, electron configuration.","duration":"2–3 hours"},
        {"step":2,"title":"Periodic Table & Bonding","desc":"Periodic trends, ionic, covalent, and metallic bonds.","duration":"3–4 hours"},
        {"step":3,"title":"Chemical Reactions","desc":"Balancing equations, stoichiometry, types of reactions.","duration":"3–4 hours"},
        {"step":4,"title":"States of Matter","desc":"Solids, liquids, gases, gas laws, intermolecular forces.","duration":"2–3 hours"},
        {"step":5,"title":"Organic Chemistry","desc":"Functional groups, hydrocarbons, nomenclature, reactions.","duration":"4–5 hours"},
        {"step":6,"title":"Chemistry Lab Project","desc":"Design an experiment or solve a multi-step synthesis problem.","duration":"3–4 hours"},
    ],
    "English Literature": [
        {"step":1,"title":"Literary Devices","desc":"Metaphor, simile, imagery, symbolism, irony, allusion.","duration":"2–3 hours"},
        {"step":2,"title":"Prose Analysis","desc":"Close reading of novels and short stories. Theme, character, setting.","duration":"3–4 hours"},
        {"step":3,"title":"Poetry Study","desc":"Meter, rhyme, sonnet forms, free verse, close reading poems.","duration":"2–3 hours"},
        {"step":4,"title":"Drama & Shakespeare","desc":"Play structure, dramatic techniques, Shakespeare's key works.","duration":"3–4 hours"},
        {"step":5,"title":"Critical Writing","desc":"How to write essays: thesis, evidence, analysis, conclusion.","duration":"3–4 hours"},
        {"step":6,"title":"Comparative Essay","desc":"Compare two literary works in a structured analytical essay.","duration":"4–5 hours"},
    ],
    "History": [
        {"step":1,"title":"Ancient Civilizations","desc":"Egypt, Greece, Rome, Mesopotamia — foundations of civilization.","duration":"3–4 hours"},
        {"step":2,"title":"Medieval World","desc":"Feudalism, the Crusades, Islamic Golden Age, Black Death.","duration":"3–4 hours"},
        {"step":3,"title":"Age of Exploration","desc":"European exploration, colonialism, and its global impact.","duration":"2–3 hours"},
        {"step":4,"title":"Revolutionary Era","desc":"American Revolution, French Revolution, Industrial Revolution.","duration":"3–4 hours"},
        {"step":5,"title":"20th Century World","desc":"WWI, WWII, Cold War, decolonization, and globalization.","duration":"4–5 hours"},
        {"step":6,"title":"Historical Analysis Essay","desc":"Write a structured essay analyzing a major historical event.","duration":"3–4 hours"},
    ],
    "Cybersecurity": [
        {"step":1,"title":"Security Fundamentals","desc":"CIA triad, threats, vulnerabilities, attack vectors, security policies.","duration":"2–3 hours"},
        {"step":2,"title":"Network Security","desc":"Firewalls, VPNs, IDS/IPS, packet analysis, network protocols.","duration":"3–4 hours"},
        {"step":3,"title":"Cryptography","desc":"Symmetric/asymmetric encryption, hashing, PKI, TLS/SSL.","duration":"3–4 hours"},
        {"step":4,"title":"Ethical Hacking Basics","desc":"Reconnaissance, scanning, exploitation basics. Kali Linux tools.","duration":"4–5 hours"},
        {"step":5,"title":"Web Security","desc":"OWASP Top 10, SQL injection, XSS, CSRF, secure coding.","duration":"3–4 hours"},
        {"step":6,"title":"CTF Challenge","desc":"Solve a Capture The Flag challenge to apply all skills.","duration":"4–6 hours"},
    ],
    "Cloud Computing": [
        {"step":1,"title":"Cloud Concepts","desc":"IaaS, PaaS, SaaS, public/private/hybrid cloud, key benefits.","duration":"2–3 hours"},
        {"step":2,"title":"AWS/Azure/GCP Basics","desc":"Core services: compute, storage, networking on major platforms.","duration":"3–4 hours"},
        {"step":3,"title":"Containers & Docker","desc":"Docker basics, images, containers, Dockerfile, Docker Compose.","duration":"3–4 hours"},
        {"step":4,"title":"Kubernetes Orchestration","desc":"Pods, deployments, services, scaling, cluster management.","duration":"4–5 hours"},
        {"step":5,"title":"CI/CD & DevOps","desc":"Pipelines, Jenkins, GitHub Actions, automated deployment.","duration":"3–4 hours"},
        {"step":6,"title":"Cloud Project Deployment","desc":"Deploy a full application on a cloud platform with monitoring.","duration":"5–6 hours"},
    ],
}

@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET","POST"])
def login():
    error = None
    if request.method == "POST":
        u = request.form.get("username","").strip()
        p = request.form.get("password","").strip()
        if u in USERS and USERS[u]["password"] == p:
            session["username"] = u
            session["name"] = USERS[u]["name"]
            return redirect(url_for("dashboard"))
        error = "Invalid username or password."
    return render_template("login.html", error=error)

@app.route("/register", methods=["GET","POST"])
def register():
    error = None
    if request.method == "POST":
        name = request.form.get("name","").strip()
        email = request.form.get("email","").strip()
        u = request.form.get("username","").strip()
        p = request.form.get("password","").strip()
        if not all([name, email, u, p]):
            error = "All fields are required."
        elif u in USERS:
            error = "Username already taken."
        elif len(p) < 6:
            error = "Password must be at least 6 characters."
        else:
            USERS[u] = {"password": p, "name": name, "email": email}
            session["username"] = u
            session["name"] = name
            return redirect(url_for("dashboard"))
    return render_template("register.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    subjects = list(QUIZZES.keys())
    return render_template("dashboard.html", name=session["name"], subjects=subjects)

@app.route("/quiz/<subject>")
def quiz(subject):
    if "username" not in session:
        return redirect(url_for("login"))
    if subject not in QUIZZES:
        return redirect(url_for("dashboard"))
    path = LEARNING_PATHS.get(subject, [])
    total = len(QUIZZES[subject])
    return render_template("quiz.html", subject=subject, path=path,
                           name=session["name"], total=total)

@app.route("/api/question", methods=["POST"])
def api_question():
    if "username" not in session:
        return jsonify({"error": "unauthorized"}), 401
    data = request.get_json()
    subject = data.get("subject","Python Programming")
    exclude = data.get("exclude", [])
    pool = QUIZZES.get(subject, QUIZZES["Python Programming"])
    available = [(i, q) for i, q in enumerate(pool) if i not in exclude]
    if not available:
        available = list(enumerate(pool))
    idx, q = random.choice(available)
    return jsonify({"idx": idx, "question": q["question"],
                    "options": q["options"], "total": len(pool)})

@app.route("/api/answer", methods=["POST"])
def api_answer():
    if "username" not in session:
        return jsonify({"error": "unauthorized"}), 401
    data = request.get_json()
    subject = data.get("subject")
    idx = data.get("idx")
    chosen = data.get("chosen")
    pool = QUIZZES.get(subject, [])
    if idx is None or idx >= len(pool):
        return jsonify({"error":"invalid"}), 400
    q = pool[idx]
    correct = q["answer"]
    return jsonify({
        "correct": correct == chosen,
        "correct_index": correct,
        "explanation": q["explanation"]
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
