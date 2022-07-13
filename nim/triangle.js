function makeTriangle(len)
{
   for (let i = 1; i <= len; i++) 
   {
      for (let j = 1; j <= i; j++) 
      {
        console.log('*');
      }
      console.log("\n");
   }
}
makeTriangle(10);