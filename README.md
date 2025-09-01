# 💾 Distributed Sharded Database System 💾

Explore a hands-on implementation of a distributed key-value storage system with **sharding**, **replication**, and **fault-tolerant features**! 🚀

---

## 🎯 Project Overview
This project demonstrates a **distributed database system** where multiple nodes store data and a **Shard Master** manages the distribution. It allows:

- Dynamic addition/removal of nodes
- Automatic key redistribution
- Fault detection
- Vertical & horizontal scalability ⚡

The system is built for **efficient access**, **balanced load**, and **resilient operations** in multi-node environments.

---

## 🛠️ System Architecture

**Shard Master**  
- Controls key assignment and node ranges  
- Redistributes keys when nodes join or leave  

**KVStorage Nodes**  
- Each node stores keys in memory  
- Can transfer or redistribute keys to other nodes  

**Clients**  
- Communicate with the Shard Master via gRPC to read/write data  

**Fault-Tolerant Mechanisms**  
- Replica groups detect failures automatically  
- Leader election (Paxos or Raft) ensures a new replica master is chosen if necessary  

---

## 💡 Key Features
- **Dynamic shard allocation** for balanced load  
- **Adding/removing nodes** on the fly  
- **Horizontal & vertical scalability**  
- **Automatic detection and recovery** from node failures  
- **Synchronized key redistribution** between nodes  

---

## 🔍 How It Works
1. **Client Requests**: Clients send queries or updates via gRPC  
2. **Shard Master Management**: Determines which node is responsible for each key and manages redistribution when the system changes  
3. **KVStorage Operations**: Nodes store keys, transfer data, and synchronize as instructed by the Shard Master  
4. **Fault Tolerance**: Heartbeats detect failures; consensus algorithms elect new replica masters when needed  

---

## 📚 Learning Goals
- Understand **distributed client-server communication**  
- Implement **sharding** for load balancing  
- Apply **fault-tolerant techniques** and **leader election**  
- Gain experience with **gRPC**, **key redistribution**, and **replication**  

---

## 🌐 Real-World Inspirations
**MongoDB**  
- Sharded NoSQL database with shard clusters, config servers, and Mongos routers  

**Apache Cassandra**  
- Ring-based architecture with replication, distributed nodes, and consensus-based consistency  

---

## 📈 Takeaways
- Scalable **distributed system architecture**  
- Dynamic **data redistribution**  
- **Fault tolerance** in multi-node environments  
- Hands-on practice with **distributed algorithms** and **gRPC**  

---

## 🙌 Contributions & Credits
Implemented as part of a **Distributed Systems course project**.  
Thanks to open-source technologies and concepts that guided this implementation: **Python, gRPC, Paxos/Raft consensus**.  

---

## 📫 Contact & Support
Questions or discussions? Open an issue or reach out! ✉️  

Thank you for checking out this project! 🚀  
Learn, experiment, and build **resilient distributed systems**! 🌐💡
