using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Stripe;

namespace StripeApp
{
    class StripeOps
    {
        // Should log it..
        private static void StripeExceptionHandler(StripeException e)
        {
            switch (e.StripeError.ErrorType)
            {
                case "card_error":
                    Console.WriteLine("   Code: " + e.StripeError.Code);
                    Console.WriteLine("Message: " + e.StripeError.Message);
                    break;
                case "api_connection_error":
                    break;
                case "api_error":
                    break;
                case "authentication_error":
                    break;
                case "invalid_request_error":
                    break;
                case "idempotency_error":
                    break;
                case "rate_limit_error":
                    break;
                case "validation_error":
                    break;
                default:
                    // Unknown Error Type
                    break;
            }
        }

        // Get a charge objects starting from fd to td (both inclusive, in UTC)
        // Returns List of StripeCharge
        public static List<StripeCharge> GetStripeChargeList(DateTime fd, DateTime td)
        {
            List<StripeCharge> chargeItems = new List<StripeCharge>();
            var chargeService = new StripeChargeService();
            bool noErr = true;

            // get some filtering
            // '2017-12-13 00:00:00', '2017-12-13 23:59:59'
            var opt = new StripeChargeListOptions();
            opt.Limit = 20;
            opt.IncludeTotalCount = true;
            opt.Created = new StripeDateFilter()
            {
                GreaterThanOrEqual = fd, //new DateTime(2017, 12, 13, 0, 0, 0, DateTimeKind.Utc),
                LessThanOrEqual = td     //new DateTime(2017, 12, 13, 23, 59, 59, DateTimeKind.Utc)
            };

            while (noErr)
            {
                StripeList<StripeCharge> s = null;
                try
                {
                    s = chargeService.List(opt);
                    chargeItems.AddRange(s.Data); 
                    if (s.HasMore)
                    {
                        // get the object id of last item, so that next loop will fetch
                        // from that id onwards, until limit..
                        // int count = s.Data.Count;
                        // opt.StartingAfter = s.Data[count - 1].Id;
                        opt.StartingAfter = s.LastOrDefault().Id;
                    }
                    else
                    {
                        noErr = false;
                    }
                }
                catch (StripeException e)
                {
                    StripeExceptionHandler(e);
                    noErr = false;
                }
                catch (Exception exp)
                {
                    Console.WriteLine(exp.Message);
                    noErr = false;
                }
            }

            return chargeItems;
        }


    } // end class
}
