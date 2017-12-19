using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.IO;
using System.Reflection;
using Stripe;

namespace StripeApp
{
    class OutputCSV
    {
        public static void GenerateCSV(List<StripeCharge> list, DateTime date)
        {
            string Filename = "stripe_" + date.ToString("MM_dd_yyyy_HH_mm_ss") + ".csv";
            StringBuilder sb = new StringBuilder();

            try
            {
                using (StreamWriter Writer = new StreamWriter(Filename, false, Encoding.UTF8))
                {
                    foreach (StripeCharge c in list)
                    {
                        string text = c.Id + "," + c.Description + "," + c.Created + "," +
                            c.Amount + "," + c.AmountRefunded + "," + c.Currency + "," +
                            c.ApplicationFee + "," + c.Status + "," + c.Captured;
                        sb.AppendLine(text);
                    }

                    Writer.WriteLine(sb.ToString());
                }
            }
            catch
            {
                throw;
            }
        }
    }
}
