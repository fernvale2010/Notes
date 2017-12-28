/*
 * Created by SharpDevelop.
 * User: songgeelim
 * Date: 9/11/2017
 * Time: 4:21 PM
 * 
 * To change this template use Tools | Options | Coding | Edit Standard Headers.
 */
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using TestList;
using Encryption;
using System.Text.RegularExpressions;
using System.Reflection;
using System.Diagnostics;
using System.IO.Pipes;

namespace TestList
{
    class Program
    {
        public static void Main(string[] args)
        {
            MainTest6(args);
            
            Console.Write("Press any key to continue . . . ");
            Console.ReadKey(true);
        }
        
        
        // Named pipe inter-process with python app
        // http://jonathonreinhart.blogspot.sg/2012/12/named-pipes-between-c-and-python.html
        //
//import time
//import struct
//
//f = open(r'\\.\pipe\NPtest', 'r+b', 0)
//i = 1
//
//while True:
//    s = 'Message[{0}]'.format(i)
//    i += 1
//
//    print(type(s))
//        
//    f.write(struct.pack('I', len(s)))
//    f.write(s.encode('utf-8'))   # Write str length and str
//    f.seek(0)                               # EDIT: This is also necessary
//    print('Wrote:', s)
//
//    n = f.read(4)    # Read str length
//    s = f.read(n[0])                           # Read str
//    f.seek(0)                               # Important!!!
//    print('Read:', s.decode('utf-8'))
//
//    time.sleep(2)        
//        
        public static void MainTest6(string[] args)
        {
            // Open the named pipe.
            var server = new NamedPipeServerStream("NPtest");

            Console.WriteLine("Waiting for connection...");
            server.WaitForConnection();

            Console.WriteLine("Connected.");
            var br = new BinaryReader(server);
            var bw = new BinaryWriter(server);

            while (true) 
            {
                try 
                {
                    var len = (int) br.ReadUInt32();            // Read string length
                    var str = new string(br.ReadChars(len));    // Read string

                    Console.WriteLine("Read: \"{0}\"", str);

                    str = new string(str.Reverse().ToArray());  // Just for fun

                    var buf = Encoding.ASCII.GetBytes(str);     // Get ASCII byte array
                    bw.Write((uint) buf.Length);                // Write string length
                    bw.Write(buf);                              // Write string
                    Console.WriteLine("Wrote: \"{0}\"", str);
                }
                catch (EndOfStreamException) 
                {
                    break;                    // When client disconnects
                }
            }

            Console.WriteLine("Client disconnected.");
            br.Close();
            bw.Close();
            server.Close();
            server.Dispose();
        }
        
        
        
        public static void MainTest5(string[] args)
        {
            string sourceDir = ".\\";
            GetFileList(sourceDir);
            
            Console.WriteLine("--------------------------");
            
            // C:\work\SharpDevelop\TestList\TestList\bin\Debug
            Console.WriteLine(Directory.GetCurrentDirectory());
            Console.WriteLine(System.IO.Directory.GetCurrentDirectory());
            Console.WriteLine(System.IO.Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location));
            Console.WriteLine(System.IO.Path.GetDirectoryName(Assembly.GetEntryAssembly().Location));            
            string str = System.IO.Path.GetDirectoryName(Process.GetCurrentProcess().MainModule.FileName);
            Console.WriteLine(str);
            
            Console.WriteLine("--------------------------");
            
            // C:\work\SharpDevelop\TestList\TestList\bin\Debug\
            Console.WriteLine(AppDomain.CurrentDomain.BaseDirectory);
            
            Console.WriteLine("--------------------------");
            
            // C:\work\SharpDevelop\TestList\TestList\bin\Debug\TestList.exe
            Console.WriteLine(Assembly.GetEntryAssembly().Location);
            Console.WriteLine(Assembly.GetExecutingAssembly().Location);
            
            Console.WriteLine("--------------------------");

            // use Path.Combine.. files contains path also..
            string[] files = Directory.GetFiles(sourceDir);
            for (int i = 0; i < files.Length; i++)
            {
                string fileName = System.IO.Path.GetFileName(files[i]); // get filename without path
                var destination = Path.Combine(sourceDir, "File", fileName);
                Console.WriteLine(fileName + ", " + destination);
                
                // NOTE: To move the files, the destination Folder must exist, otherwise will
                //       get an exception.
                // File.Move(fileName, destination);
            }
            
            
            // creates a text file, write some lines to it..
            FileInfo fileInfo = new FileInfo("testfile.txt");
            using(StreamWriter sw = fileInfo.CreateText())
            {
                for (int i=0; i<10; i++)
                {
                    sw.WriteLine("This is line {0}", i);
                }
            }
        }
        
        // Test file move..
        public static void MainTest4(string[] args)
        {
            string source = "eclipse-jee-oxygen-1a-win32.zip";
            string destination = "eclipse-jee-oxygen-1a-win32.cpy";
            
            for (int i=0; i<20; i++)
            {
                try
                {
                    MoveTime(source, destination);
                    MoveTime(destination, source);
                }
                catch
                {
                    
                }
            }
        }
        
        public static void MainTest3(string[] args)
        {
            string findstr = @"CAN (metadata)";
            
            string filePath = @"payments-ezlink.csv";
            
            while(false)
            {
                string teststr = @"the,quick,brown,,,,fox,jumps,over,,CAN (metadata),the,lazy,dog";
                string nstr = @"the,123,nothing,,,,fox,,over,,,the,what,ever";
                
                int j = teststr.Count(c => c == ',');
                Console.WriteLine("Number of commas: " + j);
                
                int first = teststr.IndexOf(findstr);
                string str2 = teststr.Substring(0, first);
                Console.WriteLine(str2);
                
                j = str2.Count(c => c == ',');
                
                int idx = NthIndexOf(nstr, ",", j);
                var nn= nstr.Insert(idx + 1, "@@@@");
                Console.WriteLine(nn);
                break;  // run one time only
            }
            
//	        Console.ReadLine();
            
            while(true)
            {
                string n = File.ReadLines(filePath).First();
                Console.WriteLine(n);
                int first = n.IndexOf(findstr);
                string str2 = n.Substring(0, first);
                Console.WriteLine(str2);
                
                int j = str2.Count(c => c == ',');
                Console.WriteLine("Number of commas: " + j);
                
                List<string> mod = new List<string>();
                mod.Add(File.ReadLines(filePath).First());
                foreach(var line in File.ReadAllLines(filePath).Skip(1))
                {
                    int idx = NthIndexOf(line, ",", j);
                    if (idx > 0)
                    {
                        mod.Add(line.Insert(idx + 1, "\t"));
                    }
                }
                
                File.WriteAllLines("newpay2.csv", mod);
                break;
            }
        }

        // encrypt/decrypt test
        public static void MainTest2(string[] args)
        {
            string rawString = "Hello Today";
            string encryptStr = DataEncryption.EncryptData(rawString, ReadKey(AppDomain.CurrentDomain.BaseDirectory + "\\Publickey.xml"));
            string decryptStr = DataEncryption.DecryptData(encryptStr, ReadKey(AppDomain.CurrentDomain.BaseDirectory + "\\Privatekey.xml"));
            
            string connectStr = "0F603A4566F0F46A19332C9E130ACA6C97E4138D" +
                "A5A7C374B2B076D31DF17FF0D51AE7AB972BEEEC" +
                "437458E5DBAC3A6D290C2DA125C049D1EFA53833" +
                "9812DD7FBAC567F05546DF94972D2BCB0019655F" +
                "71EF0A244BB05A7DE2E58F45725AC44FF8FE010F" +
                "31F66695260A7BCC30875808DBFC4066D208B58A" +
                "0DC50F0101BBCC2AEAEB085949BAD1BD1ECC1514" +
                "09596666BAC283EEA39464DFD7C10E2117DCFF7D" +
                "B0C65456E56FF6CAF03030645B9AA681A7174AA7" +
                "38A18A555BEBEA66D8574C78EB4CA3CF2CF9A3FC" +
                "0D8CB9861DABEF25A3DFB3151B407D61F86D1B2A" +
                "1979091B2D68ACB9E13C150536AD31CC1E87CF59" +
                "A087908F0A22B2B98629A0793C5E6CD0";
            
            string connectStr2 = "5F9F543CB8D99C5327CC65806C5E304EEE0F6A11" +
                "ABFEBD3EC365917CEB43E6C442C4081CCE76428C" +
                "79CBD4B850D1434F92057328049A5FB18CAB0A2D" +
                "BA6A99E36E1964410F4F021C101E7BB9D9F373FE" +
                "20431D71E2D1E5ECBD394ED3BBBFA74FB8DC82E9" +
                "B279CEBA1B4950674DAC0DA695BA90EAE0C03F91" +
                "F81E33F2BEF812953B5EF95C98BB4549E32891D3" +
                "909B224EF8CD0CD23FC54411EF1BFBA0A31A8734" +
                "162DFA78F0E6FD03EBB0A974AFACD1A6C88FDA05" +
                "E5F4B3AC585642F3968609F15D56E628A5D2011E" +
                "D15E853DFBB36B49E00D60E64A601C12DA6C3814" +
                "60183D0B6D17FF8451FD9FC13C768EDB7C000C4B" +
                "A83945F52D517212528A2313AF4C366B";
            
            string decryptConnectStr = DataEncryption.DecryptData(connectStr, ReadKey(AppDomain.CurrentDomain.BaseDirectory + "\\Privatekey.xml"));
            string decryptConnectStr2 = DataEncryption.DecryptData(connectStr2, ReadKey(AppDomain.CurrentDomain.BaseDirectory + "\\Privatekey.xml"));

            Console.WriteLine(rawString);
            Console.WriteLine(encryptStr);
            Console.WriteLine(decryptStr);
            Console.WriteLine(decryptConnectStr);
            Console.WriteLine(decryptConnectStr2);
        }
        
        public static void MainTest1(string[] args)
        {
            SimpleLogger logger = new SimpleLogger();
            
            Console.WriteLine("Hello World!");
            
            logger.Info("==================================");
            
            List<Class1> listClass1 = new List<Class1>();
            for(int i=0; i<20; i++)
            {
                Class1 cls1 = new Class1();
                cls1.ID = 120000 + i;
                cls1.NAME = cls1.ID + "-NAME";
                cls1.JOB_NUM = cls1.ID + "-JOBNUM";
                
                listClass1.Add(cls1);
                logger.Info("1. ID = " + UniqueID.GetRefId(cls1));
            }
            
            logger.Info("-----------------------------------");
            
            foreach(Class1 n in listClass1)
            {
                logger.Info(n.ID + " " + n.JOB_NUM);
                logger.Info("2. ID = " + UniqueID.GetRefId(n));
            }
            
            logger.Info("************************************");
            
            foreach(Class1 n in listClass1)
            {
                n.JOB_NUM = n.GetRefId().ToString();
                logger.Info("2. ID = " + UniqueID.GetRefId(n));
                logger.Info("2. JN = " + n.JOB_NUM);
            }
            
            
            #if (false)
            
            DateTime datetime = DateTime.MinValue.AddDays(3);
            Console.WriteLine(datetime);  // 4/1/0001 12:00:00 AM
            
            // TODO: Implement Functionality Here
            List<Class1> listClass1 = new List<Class1>();
            for(int i=0; i<20; i++)
            {
                Class1 cls1 = new Class1();
                cls1.ID = 120000 + i;
                cls1.NAME = cls1.ID + "-NAME";
                cls1.JOB_NUM = cls1.ID + "-JOBNUM";
                
                listClass1.Add(cls1);
            }
            
            // this returns reference to object that matches
            IEnumerable<Class1> listcls = listClass1.Where(a => a.ID == 120003);
            if (listcls.Any())
            {
                Class1 ncls = listcls.FirstOrDefault();
                ncls.JOB_NUM = "Just Changed";
            }
            
            // Now print out listClass1 to see whether the record with ID of 120003 has its JOB_NUM changed..
            foreach(Class1 n in listClass1)
            {
                Console.WriteLine(n.ID + " " + n.JOB_NUM);
            }
            
            Console.WriteLine("Removing the element with JOB_NUM == 'Just Changed'");
            
            listcls = listClass1.Where(a => a.JOB_NUM == "Just Changed");
            if (listcls.Any())
            {
                Class1 ncls = listcls.FirstOrDefault();
                listClass1.Remove(ncls);
            }
            
            Console.WriteLine("Removed the element");
            
            // Now print out listClass1 again
            foreach(Class1 n in listClass1)
            {
                Console.WriteLine(n.ID + " " + n.JOB_NUM);
            }
            
            #endif
        }

        private static string ReadKey(string fileName)
        {
            StreamReader stream = new StreamReader(fileName);
            string key = stream.ReadToEnd();
            stream.Close();
            return key;
        }
        
        static IEnumerable<Tuple<int,string>> CountOccurences(IEnumerable<string> data)
        {
            return data.GroupBy(t => t).Select(t => Tuple.Create(t.Count(),t.Key));
        }
        
        public static int NthIndexOf(string target, string value, int n)
        {
            // "/((s).*?){n}/"
            Match m = Regex.Match(target, "((" + Regex.Escape(value) + ").*?){" + n + "}");

            if (m.Success)
                return m.Groups[2].Captures[n - 1].Index;
            else
                return -1;
        }
        
        
//		https://www.codeproject.com/Tips/777322/A-Faster-File-Copy
        /// &lt;summary> Time the Move
        /// &lt;/summary>
        /// &lt;param name="source">Source file path&lt;/param>
        /// &lt;param name="destination">Destination file path&lt;/param>
        public static void MoveTime (string source, string destination)
        {
            DateTime start_time = DateTime.Now;
            FMove2 (source, destination);
            long size = new FileInfo (destination).Length;
            int milliseconds = 1 + (int) ((DateTime.Now - start_time).TotalMilliseconds);
            // size time in milliseconds per hour
            long tsize = size * 3600000 / milliseconds;
            tsize = tsize / (int) Math.Pow (2, 30);
            Console.WriteLine (tsize + "GB/hour");
        }

        /// &lt;summary> Fast file move with big buffers
        /// &lt;/summary>
        /// &lt;param name="source">Source file path&lt;/param>
        /// &lt;param name="destination">Destination file path&lt;/param>
        static void FMove (string source, string destination)
        {
            int array_length = (int) Math.Pow (2, 19);  // 524288
            byte[] dataArray = new byte[array_length];
            using (FileStream fsread = new FileStream
                   (source, FileMode.Open, FileAccess.Read, FileShare.None, array_length))
            {
                using (BinaryReader bwread = new BinaryReader (fsread))
                {
                    using (FileStream fswrite = new FileStream
                           (destination, FileMode.Create, FileAccess.Write, FileShare.None, array_length))
                    {
                        using (BinaryWriter bwwrite = new BinaryWriter (fswrite))
                        {
                            for (; ; )
                            {
                                int read = bwread.Read (dataArray, 0, array_length);
                                if (0 == read)
                                    break;
                                bwwrite.Write (dataArray, 0, read);
                            }
                        }
                    }
                }
            }
            File.Delete (source);
        }
        
        // removed the BinaryReader/Writer, not sure why need these..
        static void FMove2 (string source, string destination)
        {
            int array_length = (int) Math.Pow (2, 19);  // 524288
            byte[] dataArray = new byte[array_length];
            
            using (FileStream fsread = new FileStream
                   (source, FileMode.Open, FileAccess.Read, FileShare.None, array_length))
            {
                using (FileStream fswrite = new FileStream
                       (destination, FileMode.Create, FileAccess.Write, FileShare.None, array_length))
                {
                    for (; ; )
                    {
                        int read = fsread.Read (dataArray, 0, array_length);
                        if (0 == read)
                            break;
                        fswrite.Write (dataArray, 0, read);
                    }
                }
            }
            File.Delete (source);
        }
        
        
        static void GetFileList(string dir)
        {
            try
            {
                string[] files = Directory.GetFiles(dir, "*", SearchOption.AllDirectories);
                foreach (string file in files)
                {
                    FileInfo fileInfo = new FileInfo(file);
                    Console.WriteLine(fileInfo.FullName);
                }
            }
            catch(Exception exception)
            {
                Console.WriteLine("Exception: " + exception.Message);
            }
        }
        
        
        
        
    }
}
