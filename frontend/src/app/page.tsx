import Image from "next/image";

const HomePage = () => {
  return (
    <section className="pt-12 sm:pt-15">
      <div className="px-4 mx-auto max-w-7xl sm:px-6 lg:px-8">
        <div className="text-center">
          <div className="flex justify-center items-end">
            <Image
              src="/ov.png"
              alt="OnlyVels AMS"
              width={1280}
              height={320}
              className="md:h-20 h-16 w-auto"
            />
            <span className="font-medium md:text-2xl text-xl">AMS</span>
          </div>
          <h1 className="max-w-4xl mx-auto px-6 md:text-lg mt-5 text-gray-600 font-inter">
            Welcome to OnlyVels AMS, the ultimate solution for effortless
            attendance management. Get real-time insights, detailed reports, and
            an intuitive interface to simplify tracking and managing attendance.
            Experience precision and ease like never before!
          </h1>
          <div className="px-8 sm:items-start sm:justify-center sm:px-0 sm:space-x-5 sm:flex mt-9">
            <a
              href="/login"
              className="mb-3 sm:mb-0 inline-flex items-center justify-center w-full px-8 py-3 text-lg font-bold text-white transition-all duration-200 bg-gray-900 border-2 border-transparent sm:w-auto rounded-xl hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900"
              role="button"
            >
              Login
            </a>
            <a
              href="/register"
              className="inline-flex items-center justify-center w-full px-8 py-3 text-lg font-bold text-gray-900 hover:text-white transition-all duration-200 bg-gray-100 border-2 border-gray-900 sm:w-auto rounded-xl hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-900"
              role="button"
            >
              Create an account
            </a>
          </div>
        </div>
      </div>
      <div className="bg-white">
        <div className="relative mx-auto mt-4 md:mt-8">
          <div className="lg:max-w-4xl lg:mx-auto">
            <Image
              className="px-4 md:mpx-8"
              width={1622}
              height={912}
              src="/ss.png"
              alt=""
            />
          </div>
        </div>
      </div>
      <div className="text-center flex justify-center items-center mt-12 p-3 border bt">
        <a
          href="https://github.com/0xramm/Attendance-Monitoring"
          target="_blank"
          rel="noopener noreferrer"
          className="flex justify-center items-center"
        >
          <p className="text-gray-600 mb-2 font-semibold">
            Contribute to OnlyVels
          </p>
          <Image
            className="h-5 ml-2 mb-1"
            src="/git.svg"
            width={20}
            height={20}
            alt=""
          />
        </a>
      </div>
    </section>
  );
};

export default HomePage;
