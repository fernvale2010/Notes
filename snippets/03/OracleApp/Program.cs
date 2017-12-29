using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Oracle.DataAccess.Client;
using Npgsql;
using OracleApp.Model;
using OracleApp.Model.DatabaseModel;


namespace OracleApp
{
    class Program
    {
        static void Main(string[] args)
        {
            TestPostgresql();
//            TestOracle();
            
            Console.WriteLine("Press enter to continue");
            Console.ReadLine();
        }
        
        
        static void TestOracle()
        {
            var ConnectionString = "";

            
            using (OracleConnection connection =
                   new OracleConnection())
            {
                connection.ConnectionString =
                    ConnectionString;

                try
                {
                    connection.Open();
                    Console.WriteLine
                        ("Connection Successful!");
                }
                catch (OracleException ex)
                {
                    Console.WriteLine(ex.ToString());
                }
            }
        }
        
        
        static void TestPostgresql()
        {
            //            string processingDateTimeString = DateTime.Now.AddDays(-1).ToString(Constants.ProcessingDateFormat);
            string processingDateTimeString = "20-11-15";

            //var connString = "Host=127.0.0.1;Port=5432;Username=postgres;Password=postgres;Database=postgres;";
            var connString = "Server=127.0.0.1;Port=5439;User Id=postgres;Database=postgres;";
            // Server=XX.XX.XX.XX;Port=5433;User Id=XXXX;Password=XXXX;Database=XXXX;Pooling=true;
            // MaxPoolSize=100;ConnectionLifeTime=15;Timeout=45;CommandTimeout=30;ApplicationName=ManagedAppServer;
            // SearchPath=XXXXXX;
            
            Console.WriteLine(processingDateTimeString);

            using (var conn = new NpgsqlConnection(connString))
            {
                try
                {
                    conn.Open();

                    //                // Insert some data
                    //                using (var cmd = new NpgsqlCommand())
                    //                {
                    //                    cmd.Connection = conn;
                    //                    cmd.CommandText = "INSERT INTO data (some_field) VALUES (@p)";
                    //                    cmd.Parameters.AddWithValue("p", "Hello world");
                    //                    cmd.ExecuteNonQuery();
                    //                }

                    // Retrieve all rows
                    var sql1 = "SELECT * FROM trx2_details_src8;";
                    var sql2 = "select cardno as cardno, authcode as authcode, trx_date as trx_date, report_date as report_date " +
                        "from trx2_details_src8;";
                    var sql3 = "select reqref as reqref from trial;";
                    
                    using (var cmd = new NpgsqlCommand(sql3, conn))
                        using (var reader = cmd.ExecuteReader())
                    {
                        while (reader.Read())
                        {
                            // using sql2 query..
                            //Console.WriteLine(reader["cardno"] + ", " + reader["authcode"] + ", " + reader["trx_date"]);
                            Console.WriteLine(reader["reqref"]);
                        }
                    }
                    
                    IEnumerable<TX_CSC_FINANCIAL> CRecords = ReconDAL.GetCRecords(processingDateTimeString, Constants.CONST_AGENTID_ONLINE, Constants.CONST_TXN_TYPE_CD_TOPUP);
//                    if (CRecords != null && CRecords.Any())
//                    {
//                        foreach(var c in CRecords)
//                        {
//                            Console.WriteLine(c.CSC_APP_NO + ", " + c.PROCESSING_DATE.ToString());
//                            Console.WriteLine(c.PURSE_TXN_CTR);
//                        }
//                    }
                    
                    // delegate with lambda..
                    // meaning take a IEnumerable<TX_CSC_FINANCIAL> for input, and return a
                    // IEnumerable<TX_CSC_FINANCIAL>..
                    Func<IEnumerable<TX_CSC_FINANCIAL>, IEnumerable<TX_CSC_FINANCIAL>> func = cRec =>
                    {
                        var enumerable = new List<TX_CSC_FINANCIAL>();
                        
                        foreach(var c in cRec)
                        {
                            enumerable.Add(c);
                        }
                        return enumerable;
                    };
                    
                    
                    // delegate with lambda..
                    Func<IEnumerable<TX_CSC_FINANCIAL>, IEnumerable<TX_CSC_FINANCIAL>> func2 = cRec =>
                    {
                        var enumerable = cRec.Where(c => c.PURSE_TXN_CTR > 2000);

                        return enumerable;
                    };                    
                    
                    var j = func2(CRecords); // calls the delegate func
                    if (j != null && j.Any())
                    {
                        foreach(var c in j)
                        {
                            Console.WriteLine(c.CSC_APP_NO + ", " + c.TXN_DATETIME.ToString());
                            Console.WriteLine(c.PURSE_TXN_CTR);
                        }
                        Console.WriteLine("Count = {0}", j.Count());
                    }
                }
                catch (Exception e)
                {
                    Console.WriteLine(e.ToString());
                }
            }
        }
    }
}
