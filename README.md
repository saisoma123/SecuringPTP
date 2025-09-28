# SecuringPTP

# Motivation
Time synchronization between devices is critical in networked embedded systems. The Precision Time Protocol (PTP) provides highly accurate time synchronization (sub-microsecond accuracy) over a network (typically Ethernet) for devices in these systems. An intelligent adversary can potentially subdue an entire network through clever manipulations at the network or kernel level, which is why PTP security is paramount. The original PTP standard was designed with no security considerations in mind, and made certain network assumptions such as path symmetry and message integrity. Researchers demonstrated that this standard can be subjugated, such as implementing delay attacks that induce hundreds of microseconds of offset and exploiting the Best Master Clock Algorithm to win the election process and broadcast a forged time reference.

Because of the risk of the aforementioned cyberattacks, the IEEE-1588 group released an improved standard with cryptographic mechanisms (symmetric-key based authentication), ensuring message integrity and protection against attacks such as spoofing and message replay. There are, of course, network-level and kernel-level attacks that it cannot protect against.

Related work has focused on exploring these network-level vulnerabilities/attacks of the new standard, and providing defensible solutions against these attacks. For example, identity spoofing attacks can still compromise symmetric-key based authentication, researchers argue that this authentication mechanism has to be replaced with elliptic-curve and public-key based cryptographic mechanisms. Also, delay attacks are still present on this standard, although there has been work [3] that augments the standard by implementing cyclic path asymmetry analysis, to detect malicious delays on PTP messages. Further work includes [4] detecting fake timestamp injection by providing a central entity that validates slave messages against master messages via encryption and bitmasking and [5] protecting against Byzantine attacks by providing clients with multiple time sources and aggregating these into an estimate of clock drift/offset. 

However, kernel-level attacks, more specifically, attacks in which an adversary has privileged access to the host running the PTP stack, have been relatively unexplored thus far. However, there has been a study [6] to showcase that inserting in-kernel payloads for 3 attack primitives, constant offset, progressive skew, and random jitter can subvert time synchronization while passing network-level validation. This is a serious blind-spot that has not been addressed by any PTP-specific solution. However, there are more general solutions for protecting against kernel-level attacks in the context of timekeeping. More specifcally, TimeGuard [1] is a trusted timing service within Arm TrustZone that provides secure and isolated access to hardware timers, even with the presence of a privileged adversary. TimeGuard is based on an earlier framework [2] TimeSeal, which provides a trusted timing service to applications within Intel SGX.

In this work, we aim to apply the foundations and mechanisms of TimeGuard to secure PTP against kernel-level timing attacks. We will use hardware-based roots of trust that can be utilized as a trusted processor in the system. Likewise to Timeguard, we will use secure enclaves or trusted execution environments (TEE) to isolate typical PTP operations from the untrusted operating system, including message authentication, timestamping, and clock synchronization, reducing the probability of tampering or spoofing. In terms of TEE/Timeguard mechanisms, we aim to implement a TimeGuard client for the non-secure world and a TimeGuard handler/watchdog for the secure world. This design allows the client to either forward PTP messages for secure handling via the TimeGuard handler or continously monitor the control register for tampering and provide the client access to the secure time source via the TimeGuard watchdog (PTP operations would be in non-secure world in this mode). This hardens PTP, making it resilient and accurate against timing attacks. 

# Design Goals
- Hardware capable of handling PTP via secure enclave

- Designing attacker/threat model and kernel-level timing attacks to examine PTP vulnerabilities

- Designing a secure PTP time synchronization protocol 
    - Design TEE mechanisms
    - Streamline TimeGuard mechanism design for PTP

- Evaluation of the protocol against attacks

- Analysis of the protocol's overhead

- Propose defensible extensions on top of protocol

# Deliverables
- Hardware setup, SabreSD board and BeagleBone Black connected via Ethernet network

- Implementations of kernel-level timing attacks 

- Implementation of secure PTP in OP-TEE/Linux (trusted handler and watchdog/client)
    - Implementation of TEE/Timeguard mechanisms

- Characterize the network delay between the BeagleBone Black and the NXP SabreSD board

- Estimate the relative clock drift between the participating devices

- Estimate the CPU overhead of the secure PTP protocol

- (If time allowing) implementations of extensions on top of protocol for further analysis


# System Blocks

![My Diagram](SecuringPTP/images/SystemBlocks.jpg)

# HW/SW requirements
Windows PC, BeagleBone Black, NXP i.MX6Q SabreSD development board (ARM Cortex-A9 cores), ARM TrustZone hardware + OP-TEE OS (secure enclave on SabreSD board)

# Project Timeline

- Hardware Setup (1.5 weeks)
    - Setting up the BeagleBone Black and SabreSD OPTEE to run PTP
- Deploying PTP on the secure enclave (1.5 weeks)
- Exploring PTP attacks and evaluating their impact (2 weeks)
- Integrating the TimeGuard framework for PTP (2 weeks)
- Designing defense mechanisms against attacks (2 weeks)
- Evaluating the defense and analyzing its overhead (1 week)


# References

[1] Nasrullah, A., & Anwar, F. M. (2024). Trusted timing services with TimeGuard. 2024 IEEE 30th Real-Time and Embedded Technology and Applications Symposium (RTAS), 1–14

[2] Anwar, F. M., Garcia, L., Han, X., & Srivastava, M. (2019). Securing time in untrusted operating systems with TimeSeal. 2019 IEEE Real-Time Systems Symposium (RTSS), 80–92

[3] Finkenzeller, A., Butowski, O., Regnath, E., Hamad, M., & Steinhorst, S. (2024). PTPsec: Securing the precision time protocol against time delay attacks using cyclic path asymmetry analysis. arXiv preprint arXiv:2401.10664.

[4] Moussa, B., Robillard, C., Zugenmaier, A., Kassouf, M., Debbabi, M., & Assi, C. (2019). Securing the precision time protocol (PTP) against fake timestamps. IEEE Communications Letters, 23(2), 278–281.

[5] Shi, S., Xiao, Y., Du, C., Shahriar, M. H., Li, A., Zhang, N., Hou, Y. T., & Lou, W. (2023). MS-PTP: Protecting network timing from Byzantine attacks. In Proceedings of the 16th ACM Conference on Security and Privacy in Wireless and Mobile Networks (WiSec ’23) (pp. 61–71). Association for Computing Machinery.

[6] Soomro, M. A., & Anwar, F. M. (2025). Breaking precision time: OS vulnerability exploits against IEEE 1588. IEEE International Symposium on Precision Clock Synchronization for Measurement, Control, and Communication (ISPCS) 