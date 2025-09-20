export default function Button({children, className="", type="button", ...props}){
    return (
      <button
        type={type}
        className={`inline-flex items-center justify-center gap-2 rounded-xl border border-transparent px-4 py-2 text-sm font-medium shadow-sm transition active:scale-[.98] bg-indigo-600 text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 ${className}`}
        {...props}
      >
        {children}
      </button>
    );
  }