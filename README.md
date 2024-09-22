# Background
This repository was created to share the source code and results of my master thesis titled 
"The impact of programming language choice on execution time when performing virtual simulation with a
driver model - A comparison of C++ and Python performance using the open simulation interface (OSI) in esmini".

# Content
It contains the raw measurements, the filtered measurements and histograms as well tables created based on that date. It also contains one CPP, four Python driver models (which just use different data structures to store needed data, namely: class, data class, dictionary and list), one C++ esmini wrapper and one Python esmini wrapper. The driver models are based on the paper by Svaerd et al. "[Computational modeling of driver pre-crash brake response, with and without off-road glances: Parameterization using real-world crashes and near-crashes](https://www.sciencedirect.com/science/article/pii/S0001457521004644)" and a C++ example was provided by her and Volvo Cars. I modified the C++ example to work standalone and converted its logic into Python. To protect the intellectual property of Volvo Cars, the source code based on their example is removed. 
The functionality of the accumulator driver model will be described via pseudo code as comments instead. 

Thanks to people behind [esmini](https://github.com/esmini/esmini), which was utilized in this work.
