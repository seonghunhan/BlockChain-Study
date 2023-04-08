# BlockChain - Study  

## Why BlockChain?  

- 실제 DB를 운영하면서 고객 데이터를 보관하는 데 많은 책임감을 느꼈고, 보안성을 높이는 방안을 찾아보다 공부를 시작함
- 블록체인 기반에 Web3.0은 앞으로 다가올 GameChanger로써 블록체인은 서버 개발자가 기본적으로 알아야 할 소양이라고 생각함  

<br>
<br>
<br>

## How to Study?

- 유데미 Blcokchain A-Z 강의를 보며 개념을 확립함  
- IT 동아리 부원들과 스터디를 진행해 개념을 공유하고 실습을 수행  
- Python으로 진행했고, Flask를 활용하여 API를 생성하며 실습을 진행  

<br>
<br>
<br>

## what did you study  


### 블록체인

- 새로운 해시는 index, proof, prev_hash (제네시스블록은 prev를 '0'으로 정의)로 생성(아래와 같은 연산으로 진행)   
- 여기서 proof는 약간 nonce개념으로 사용된다.  
- 정해진 연산에 따라 proof를 넣고 while문으로 +1을 하면서 (선행제로가 4개나올때까지)SHA256 알고리즘을 돌린다.  
- 최종적으로 쌓인 proof(nonce)를 채굴된(새로운) 블록의 proof(nonce)로 넣는다, proof(nonce)를 계속 바꿔가며 연산하는것 -> 이게핵심! 

### 실습  
1. 블록체인을 만들고 플라스크로 배포한뒤 로컬에서 포스트맨으로 확인해본다.  
1.1) 블록을 만드는 API -> /mine_block  
1.2) 체인을 확인하는 API -> /get_chain  
1.3) 유효한 체인인지 확인하는 API -> /is_valid -> 이거는 체인의 모든 블록을 돌면서 prev가 이전블록의 hash랑 같은지 체크
하나라도 틀릴경우 유효하지 않은 체인으로 판단!  

<br>
<br>

### 암호화폐  

- 사람들이 거래한내용을 트랜잭션에 저장하고, 블록체인을 한번 채굴할때마다 트랜잭션에 기입된 내용들을 적어주고 훈코인을 1개씩 얻는것!  

- 위에서 만든 블록체인을 기반으로 암호화폐 실습(훈코인 만들기)  
- 무엇이 블록체인을 암호화폐로 만드냐 -> 트랜잭션  
- 사용자들로 하여금 채굴자들이 채굴한새로운 블록에 추가된 안전한 트랜잭션을 통해 새로운 블록에 트랜잭션을 발생 시켜 암호화폐를 교환할 수 있도록 한다  
- 트랜잭션이 모이면 채굴자가 블록을 채굴하는 동시에 모였던 트랜잭션이 해당블록에 추가되는 방식  

<br>

포스트맨 실습  
- 노드 5001,5002,5003이 서로 상호작용하는 데모 (탈중앙화된 블록체인 테스트)  
1. 3개 파이썬 파일(5001,5002,5003)을 각자 실행하고  
2. 포스트맨으로 get_chain(GET) API를 각자 포트별로(5001,5002,5003) 실행하여 블록을 1개씩 갖는다.  
(하지만 아직까지는 각자 독립적인데, 합의 과정을 거쳐서 모든 노드가 같은 채인을 갖게 할것임)  

### 중요!!!!  
3. 노드를 서로 연결하는 connect_node(POST) API -> 바디값에 각자 다른 노드(5001이면 5002,5003을 기입)를 기입하고 각자 연결(아직까지는 합의과정X)  
-> 이제 블록체인이 각자 블록을 채굴할때마다 같이 연동됨(탈중앙화)  

4. 5001에서 get_mine(GET)을 하여 생성하기  
(이때 5001은 위에서 한것과 더불어 2개를 같지만 5002,5003에서 겟체인하면 아직 1개임(합의 아직 안이루어짐))  

5. 5002에서 replace_chain(GET)하면 5001에서 추가한 블록을 가지고옴 (합의 과정)  

6. 트랜잭션보내기 add_transaction(POST)(이거는 채굴이아니고 단순 트랜잭션을 쌓기 위함임) 5001에서 5002로 10000개 보내기  

7. 이후에 5001(누구든상관X)이 mine_block(GET)을 통해 채굴하면 이전에 트랜잭션에 기입한게 올라옴(이후 초기화)  
3번째 블록의 트랜잭션에는 5번에서 보낸 기록이 명세되어있음  

8. 이제 5001이 채굴했으니까 5001의 채인은 업뎃(3개블록)되어있지만 나머지2개는 아직 합의가 안이루어짐  

9. 나머지(5002,5003)에서는 아직 2개의 블록임 그래서 합의(replace_chain)이 다시 이루어져야함  

<br>
<br>
<br>

## study review

- 개별 블록들이 1개의 체인을 이루고 각 노드들의 체인이 1개의 체인을 공유하며 탈중앙화하는것이 인상적이었다.  
- 일반적인 데이터보단 불변해야 하는 원장 데이터를 저장하기에 좋은 기술이라고 느꼈다.  
- 다음번에 기회가 된다면 로컬보다 네트워크상에서 구현해보고 싶다.  
