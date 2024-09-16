chat = """
/*
How to run
==========
save the file as chat.java (filename can be anything)
Command Prompt 1 (go to the location the file is saved)
javac *.java
java Server

Command Prompt 2 (go to the location the file is saved)
java Client
*/

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.io.*;
import java.net.*;

class Client extends JFrame{
    JTextField jt;
    JButton send;
    JLabel lbl;
    public static void main(String[] args) {
	new Client();
    }
    Client(){
        setTitle("Client");
	setSize(400, 200);
        setVisible(true);
	setLayout(new FlowLayout());
	lbl = new JLabel("Enter a string:");
        jt = new JTextField(20);
        send = new JButton("Send");
	add(lbl);
	add(jt);
	add(send);
	validate();
        send.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent ae) {
                try{
                    Socket s = new Socket("localhost", 1234);
                    DataOutputStream out = new DataOutputStream(s.getOutputStream());
                    out.writeUTF(jt.getText());
		    jt.setText("");
                    s.close();
                }catch(Exception e){System.out.println(e);}
            }
        });
    }
}

class Server extends JFrame{
    JTextArea jta;
    String newline = System.lineSeparator();
    public static void main(String[] args) {
	new Server();
    }
    Server(){
        setTitle("Server");
        setSize(400, 200);
        setVisible(true);
        jta = new JTextArea("Waiting for message..."+newline);
        add(jta);
	validate();
	try{
		ServerSocket ss = new ServerSocket(1234);
		while(true){
			Socket s = ss.accept();
	                DataInputStream in = new DataInputStream(s.getInputStream());
               		String msg = in.readUTF();
		        jta.append("Received: "+msg+" ("+check(msg)+")"+newline);
               		s.close();
                }
	}catch(Exception e){System.out.println(e);}
    }
    String check(String msg){
	StringBuffer rmsg = new StringBuffer(msg);
	rmsg.reverse();
	return msg.equalsIgnoreCase(new String(rmsg)) ? "It is a palindrome" : "It is not a palindrome";
    }
}
"""
file_transfer = """
/*
How to run
==========
save the file as filetransfer.java (filename can be anything)
Command Prompt 1 (go to the location the file is saved)
javac *.java
java Server

Command Prompt 2 (go to the location the file is saved)
java Client

select file_to_send.txt which will be there in the file location
(any file can be sent)
*/

import java.io.*;
import java.net.*;
import javax.swing.*;
import java.awt.event.*;

class Client extends JFrame {
	JTextArea jta;
	JButton send;
	JFileChooser jc;
	static String newline = System.lineSeparator();
	Client(){
		setTitle("File Client");
		setSize(400, 300);
		setVisible(true);
		jta = new JTextArea();
		send = new JButton("Send File");
		jc = new JFileChooser();
		send.addActionListener(new ActionListener(){
			public void actionPerformed(ActionEvent e){
				int op = jc.showOpenDialog(null);
				if(op == JFileChooser.APPROVE_OPTION)
					sendFile(jc.getSelectedFile());
			}
		});
		add(new JScrollPane(jta), "Center");
		add(send, "South");
		validate();
	}
	void sendFile(File f) {
		try{
			Socket s = new Socket("localhost", 5000);
			jta.setText("Connected to server"+newline);
			FileInputStream fin = new FileInputStream(f);
			OutputStream out = s.getOutputStream();

			byte[] buffer = new byte[1024];
			int bytesRead;
			while ((bytesRead = fin.read(buffer)) != -1){
				for (int i = 0; i < bytesRead; i++){
					byte plainByte = buffer[i];
					byte cipherByte = (byte) ((plainByte + 3) % 256);
					jta.append("Plain Text: " + plainByte + " (" + (char) plainByte + ") -> Cipher Text: " + cipherByte + " (" + (char) cipherByte + ")"+newline);
					buffer[i] = cipherByte;
				}
				out.write(buffer, 0, bytesRead);
			}
			fin.close();
			out.close();
			s.close();
			jta.append("File encrypted and sent successfully"+newline);
		}catch(Exception e){System.out.println(e);}
	}
	public static void main(String[] args){
		try{
			FileWriter fout = new FileWriter("file_to_send.txt");
			fout.write("Hello World"+newline+"Hello To JAVA");
			fout.close();
			new Client();
		}catch(Exception e){System.out.println(e);}
	}
}

class Server extends JFrame{
	JTextArea jta;
	String newline = System.lineSeparator();
	Server(){
		setTitle("File Server");
		setSize(400, 300);
		setVisible(true);
        	jta = new JTextArea();
        	add(new JScrollPane(jta));
		validate();
        	try{
            		ServerSocket ss = new ServerSocket(5000);
            		jta.append("Server is listening on port 5000"+newline);
	    		for(int n=1;n<=10;n++){
            			Socket s = ss.accept();
            			jta.setText("Client connected"+newline);
            			InputStream in = s.getInputStream();
            			FileOutputStream fout = new FileOutputStream("received_file_"+n+".txt");

            			byte[] buffer = new byte[1024];
            			int bytesRead;
            			while ((bytesRead = in.read(buffer)) != -1){
                			for (int i = 0; i < bytesRead; i++){
                    				byte cipherByte = buffer[i];
                    				byte plainByte = (byte) ((cipherByte - 3 + 256) % 256);
                    				jta.append("Cipher Text: " + cipherByte + " (" + (char) cipherByte + ") -> Plain Text: " + plainByte + " (" + (char) plainByte + ")"+newline);
                    				buffer[i] = plainByte;
                			}
                			fout.write(buffer, 0, bytesRead);
            			}
            			fout.close();
	            		in.close();
        	    		s.close();
	            		jta.append("File received and decrypted successfully"+newline);
			}
			ss.close();
        	}catch(Exception e){System.out.println(e);}
	}
	public static void main(String[] args){
		new Server();
	}
}
"""
rmi = """
/*
How to run
==========
save the file as rmi.java (filename can be anything)
Command Prompt 1 (go to the location the file is saved)
javac *.java
start rmiregistry
java Server

Command Prompt 2 (go to the location the file is saved)
java Client localhost

Note: If version error occurs, Compile following way:
javac --release 8 *.java
*/

import java.net.*;
import java.rmi.*;
import java.rmi.server.*;

interface MyServerIntf extends Remote{	
	String add(double a, double b) throws RemoteException;
}

class MyServerImpl extends UnicastRemoteObject implements MyServerIntf{
	MyServerImpl()throws RemoteException{}
	public String add(double a, double b)throws RemoteException{
		return a+" + "+b+" = "+(a+b);
	}	
}

class Client{
	public static void main(String[] arg){
		try{
			String name;
			if(arg.length == 0)
				name = "rmi://localhost/RMServer";
			else
				name = "rmi://"+arg[0]+"/RMServer";
			MyServerIntf asif = (MyServerIntf)Naming.lookup(name);
			System.out.println("Addition: "+asif.add(1200,1300));
		}catch(Exception e){System.out.println("Exception: "+e);}
	}
}


class Server{
	public static void main(String[] arg){
		try 	{
			MyServerImpl asi = new MyServerImpl();
			Naming.rebind("RMServer",asi);
			System.out.println("Server Started...");
		}
		catch(Exception e){System.out.println("Exception: "+e);}
	}
}
"""
rmi = """
/*
How to run
==========
save the file as rmi.java (filename can be anything)
Command Prompt 1 (go to the location the file is saved)
javac *.java
start rmiregistry
java Server

Command Prompt 2 (go to the location the file is saved)
java Client localhost

Note: If version error occurs, Compile following way:
javac --release 8 *.java
*/

import java.net.*;
import java.rmi.*;
import java.rmi.server.*;

interface MyServerIntf extends Remote{	
	String add(double a, double b) throws RemoteException;
}

class MyServerImpl extends UnicastRemoteObject implements MyServerIntf{
	MyServerImpl()throws RemoteException{}
	public String add(double a, double b)throws RemoteException{
		return a+" + "+b+" = "+(a+b);
	}	
}

class Client{
	public static void main(String[] arg){
		try{
			String name;
			if(arg.length == 0)
				name = "rmi://localhost/RMServer";
			else
				name = "rmi://"+arg[0]+"/RMServer";
			MyServerIntf asif = (MyServerIntf)Naming.lookup(name);
			System.out.println("Addition: "+asif.add(1200,1300));
		}catch(Exception e){System.out.println("Exception: "+e);}
	}
}


class Server{
	public static void main(String[] arg){
		try 	{
			MyServerImpl asi = new MyServerImpl();
			Naming.rebind("RMServer",asi);
			System.out.println("Server Started...");
		}
		catch(Exception e){System.out.println("Exception: "+e);}
	}
}
"""
wired_tcl = """
#How to run
#==========
#save this file as wired.tcl in desktop folder
#also save wired.awk file in the same location
#open desktop right-click and choose 'Open in Terminal'
#run this command
#ns wired.tcl

#both nam and awk file will be executed automatically

#create a simulator object 
set ns [new Simulator]

#create a trace file, this file is for logging purpose 
set tracefile [open wired.tr w]
$ns trace-all $tracefile

#create a animation infomration or NAM file creation
set namfile [open wired.nam w]
$ns namtrace-all $namfile

#create nodes
set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]

#creation of link between nodes with DropTail Queue
#Droptail means Dropping the tail.
$ns duplex-link $n0 $n1 5Mb 2ms DropTail
$ns duplex-link $n2 $n1 10Mb 5ms DropTail
$ns duplex-link $n1 $n4 3Mb 10ms DropTail
$ns duplex-link $n4 $n3 100Mb 2ms DropTail
$ns duplex-link $n4 $n5 4Mb 10ms DropTail

#creation of Agents
#node 0 to Node 3
set udp [new Agent/UDP]
set null [new Agent/Null]
$ns attach-agent $n0 $udp
$ns attach-agent $n3 $null
$ns connect $udp $null

#creation of TCP Agent
set tcp [new Agent/TCP]
set sink [new Agent/TCPSink]
$ns attach-agent $n2 $tcp
$ns attach-agent $n5 $sink
$ns connect $tcp $sink

#creation of Application CBR, FTP
#CBR - Constant Bit Rate (Example nmp3 files that have a CBR or 192kbps, 320kbps, etc.)
#FTP - File Transfer Protocol (Ex: To download a file from a network)
set cbr [new Application/Traffic/CBR]
$cbr attach-agent $udp

set ftp [new Application/FTP]
$ftp attach-agent $tcp

#Start the traffic 
$ns at 1.0 "$cbr start"
$ns at 2.0 "$ftp start"

$ns at 10.0 "finish"

#the following procedure will be called at 10.0 seconds 
proc finish {} {
 global ns tracefile namfile
 $ns flush-trace
 close $tracefile
 close $namfile
 puts "Executing nam file"
 exec nam wired.nam &
 exec awk -f wired.awk wired.tr &
 exit 0
}

puts "Simulation is starting..."
$ns run
"""
wired_awk = """
BEGIN{
	r1=r2=d1=d2=total=0
	ratio=tp1=tp2=0.0
}

{
	if($1 =="r" && $4 == 3 && $5=="cbr")r1++
	if($1 =="d" && $4 == 3 && $5=="cbr")d1++
	if($1 =="r" && $4 == 5 && $5=="tcp")r2++
	if($1 =="d" && $4 == 5 && $5=="tcp")d2++
}

END{
	total = r1+r2+d1+d2
	ratio = (r1+r2)*100/total
	tp1 = (r1+d1)*8/1000000
	tp2 = (r2+d2)*8/1000000
    print()
	printf("Wired-Network")
    print()
	printf("Packets Received: %d",r1+r2)
    print()
	printf("Packets Dropped : %d",d1+d2)
    print()
	printf("Packets Delivery Ratio: %f",ratio)
    print()
	printf("UDP Throughput: %f Mbps",tp1)
    print()
	printf("TCP Throughput: %f Mbps",tp2)
    print()
}
"""