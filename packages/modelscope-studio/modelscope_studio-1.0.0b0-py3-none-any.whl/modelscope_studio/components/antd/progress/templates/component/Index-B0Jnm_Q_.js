async function L() {
  window.ms_globals.initializePromise || (window.ms_globals.initializePromise = new Promise((e) => {
    window.ms_globals.initialize = () => {
      e();
    };
  })), await window.ms_globals.initializePromise;
}
async function M(e) {
  return await L(), e().then((t) => t.default);
}
function I(e) {
  const {
    gradio: t,
    _internal: i,
    ...s
  } = e;
  return Object.keys(i).reduce((o, n) => {
    const r = n.match(/bind_(.+)_event/);
    if (r) {
      const c = r[1], l = c.split("_"), _ = (...f) => {
        const p = f.map((u) => f && typeof u == "object" && (u.nativeEvent || u instanceof Event) ? {
          type: u.type,
          detail: u.detail,
          timestamp: u.timeStamp,
          clientX: u.clientX,
          clientY: u.clientY,
          targetId: u.target.id,
          targetClassName: u.target.className,
          altKey: u.altKey,
          ctrlKey: u.ctrlKey,
          shiftKey: u.shiftKey,
          metaKey: u.metaKey
        } : u);
        return t.dispatch(c.replace(/[A-Z]/g, (u) => "_" + u.toLowerCase()), {
          payload: p,
          component: s
        });
      };
      if (l.length > 1) {
        let f = {
          ...s.props[l[0]] || {}
        };
        o[l[0]] = f;
        for (let u = 1; u < l.length - 1; u++) {
          const h = {
            ...s.props[l[u]] || {}
          };
          f[l[u]] = h, f = h;
        }
        const p = l[l.length - 1];
        return f[`on${p.slice(0, 1).toUpperCase()}${p.slice(1)}`] = _, o;
      }
      const d = l[0];
      o[`on${d.slice(0, 1).toUpperCase()}${d.slice(1)}`] = _;
    }
    return o;
  }, {});
}
function S() {
}
function V(e, t) {
  return e != e ? t == t : e !== t || e && typeof e == "object" || typeof e == "function";
}
function Z(e, ...t) {
  if (e == null) {
    for (const s of t)
      s(void 0);
    return S;
  }
  const i = e.subscribe(...t);
  return i.unsubscribe ? () => i.unsubscribe() : i;
}
function y(e) {
  let t;
  return Z(e, (i) => t = i)(), t;
}
const w = [];
function g(e, t = S) {
  let i;
  const s = /* @__PURE__ */ new Set();
  function o(c) {
    if (V(e, c) && (e = c, i)) {
      const l = !w.length;
      for (const _ of s)
        _[1](), w.push(_, e);
      if (l) {
        for (let _ = 0; _ < w.length; _ += 2)
          w[_][0](w[_ + 1]);
        w.length = 0;
      }
    }
  }
  function n(c) {
    o(c(e));
  }
  function r(c, l = S) {
    const _ = [c, l];
    return s.add(_), s.size === 1 && (i = t(o, n) || S), c(e), () => {
      s.delete(_), s.size === 0 && i && (i(), i = null);
    };
  }
  return {
    set: o,
    update: n,
    subscribe: r
  };
}
const {
  getContext: P,
  setContext: j
} = window.__gradio__svelte__internal, B = "$$ms-gr-antd-slots-key";
function G() {
  const e = g({});
  return j(B, e);
}
const H = "$$ms-gr-antd-context-key";
function J(e) {
  var c;
  if (!Reflect.has(e, "as_item") || !Reflect.has(e, "_internal"))
    throw new Error("`as_item` and `_internal` is required");
  const t = T(), i = W({
    slot: void 0,
    index: e._internal.index,
    subIndex: e._internal.subIndex
  });
  t && t.subscribe((l) => {
    i.slotKey.set(l);
  }), Q();
  const s = P(H), o = ((c = y(s)) == null ? void 0 : c.as_item) || e.as_item, n = s ? o ? y(s)[o] : y(s) : {}, r = g({
    ...e,
    ...n
  });
  return s ? (s.subscribe((l) => {
    const {
      as_item: _
    } = y(r);
    _ && (l = l[_]), r.update((d) => ({
      ...d,
      ...l
    }));
  }), [r, (l) => {
    const _ = l.as_item ? y(s)[l.as_item] : y(s);
    return r.set({
      ...l,
      ..._
    });
  }]) : [r, (l) => {
    r.set(l);
  }];
}
const A = "$$ms-gr-antd-slot-key";
function Q() {
  j(A, g(void 0));
}
function T() {
  return P(A);
}
const R = "$$ms-gr-antd-component-slot-context-key";
function W({
  slot: e,
  index: t,
  subIndex: i
}) {
  return j(R, {
    slotKey: g(e),
    slotIndex: g(t),
    subSlotIndex: g(i)
  });
}
function ge() {
  return P(R);
}
function $(e) {
  return e && e.__esModule && Object.prototype.hasOwnProperty.call(e, "default") ? e.default : e;
}
var U = {
  exports: {}
};
/*!
	Copyright (c) 2018 Jed Watson.
	Licensed under the MIT License (MIT), see
	http://jedwatson.github.io/classnames
*/
(function(e) {
  (function() {
    var t = {}.hasOwnProperty;
    function i() {
      for (var n = "", r = 0; r < arguments.length; r++) {
        var c = arguments[r];
        c && (n = o(n, s(c)));
      }
      return n;
    }
    function s(n) {
      if (typeof n == "string" || typeof n == "number")
        return n;
      if (typeof n != "object")
        return "";
      if (Array.isArray(n))
        return i.apply(null, n);
      if (n.toString !== Object.prototype.toString && !n.toString.toString().includes("[native code]"))
        return n.toString();
      var r = "";
      for (var c in n)
        t.call(n, c) && n[c] && (r = o(r, c));
      return r;
    }
    function o(n, r) {
      return r ? n ? n + " " + r : n + r : n;
    }
    e.exports ? (i.default = i, e.exports = i) : window.classNames = i;
  })();
})(U);
var ee = U.exports;
const E = /* @__PURE__ */ $(ee), {
  SvelteComponent: te,
  assign: ne,
  check_outros: se,
  component_subscribe: x,
  create_component: ie,
  destroy_component: oe,
  detach: X,
  empty: Y,
  flush: b,
  get_spread_object: O,
  get_spread_update: re,
  group_outros: le,
  handle_promise: ce,
  init: ue,
  insert: D,
  mount_component: ae,
  noop: m,
  safe_not_equal: _e,
  transition_in: k,
  transition_out: v,
  update_await_block_branch: fe
} = window.__gradio__svelte__internal;
function q(e) {
  let t, i, s = {
    ctx: e,
    current: null,
    token: null,
    hasCatch: !1,
    pending: pe,
    then: de,
    catch: me,
    value: 17,
    blocks: [, , ,]
  };
  return ce(
    /*AwaitedProgress*/
    e[2],
    s
  ), {
    c() {
      t = Y(), s.block.c();
    },
    m(o, n) {
      D(o, t, n), s.block.m(o, s.anchor = n), s.mount = () => t.parentNode, s.anchor = t, i = !0;
    },
    p(o, n) {
      e = o, fe(s, e, n);
    },
    i(o) {
      i || (k(s.block), i = !0);
    },
    o(o) {
      for (let n = 0; n < 3; n += 1) {
        const r = s.blocks[n];
        v(r);
      }
      i = !1;
    },
    d(o) {
      o && X(t), s.block.d(o), s.token = null, s = null;
    }
  };
}
function me(e) {
  return {
    c: m,
    m,
    p: m,
    i: m,
    o: m,
    d: m
  };
}
function de(e) {
  let t, i;
  const s = [
    {
      style: (
        /*$mergedProps*/
        e[0].elem_style
      )
    },
    {
      className: E(
        /*$mergedProps*/
        e[0].elem_classes,
        "ms-gr-antd-progress"
      )
    },
    {
      id: (
        /*$mergedProps*/
        e[0].elem_id
      )
    },
    /*$mergedProps*/
    e[0].props,
    I(
      /*$mergedProps*/
      e[0]
    ),
    {
      slots: (
        /*$slots*/
        e[1]
      )
    },
    {
      percent: (
        /*$mergedProps*/
        e[0].props.percent ?? /*$mergedProps*/
        e[0].percent
      )
    }
  ];
  let o = {};
  for (let n = 0; n < s.length; n += 1)
    o = ne(o, s[n]);
  return t = new /*Progress*/
  e[17]({
    props: o
  }), {
    c() {
      ie(t.$$.fragment);
    },
    m(n, r) {
      ae(t, n, r), i = !0;
    },
    p(n, r) {
      const c = r & /*$mergedProps, $slots*/
      3 ? re(s, [r & /*$mergedProps*/
      1 && {
        style: (
          /*$mergedProps*/
          n[0].elem_style
        )
      }, r & /*$mergedProps*/
      1 && {
        className: E(
          /*$mergedProps*/
          n[0].elem_classes,
          "ms-gr-antd-progress"
        )
      }, r & /*$mergedProps*/
      1 && {
        id: (
          /*$mergedProps*/
          n[0].elem_id
        )
      }, r & /*$mergedProps*/
      1 && O(
        /*$mergedProps*/
        n[0].props
      ), r & /*$mergedProps*/
      1 && O(I(
        /*$mergedProps*/
        n[0]
      )), r & /*$slots*/
      2 && {
        slots: (
          /*$slots*/
          n[1]
        )
      }, r & /*$mergedProps*/
      1 && {
        percent: (
          /*$mergedProps*/
          n[0].props.percent ?? /*$mergedProps*/
          n[0].percent
        )
      }]) : {};
      t.$set(c);
    },
    i(n) {
      i || (k(t.$$.fragment, n), i = !0);
    },
    o(n) {
      v(t.$$.fragment, n), i = !1;
    },
    d(n) {
      oe(t, n);
    }
  };
}
function pe(e) {
  return {
    c: m,
    m,
    p: m,
    i: m,
    o: m,
    d: m
  };
}
function be(e) {
  let t, i, s = (
    /*$mergedProps*/
    e[0].visible && q(e)
  );
  return {
    c() {
      s && s.c(), t = Y();
    },
    m(o, n) {
      s && s.m(o, n), D(o, t, n), i = !0;
    },
    p(o, [n]) {
      /*$mergedProps*/
      o[0].visible ? s ? (s.p(o, n), n & /*$mergedProps*/
      1 && k(s, 1)) : (s = q(o), s.c(), k(s, 1), s.m(t.parentNode, t)) : s && (le(), v(s, 1, 1, () => {
        s = null;
      }), se());
    },
    i(o) {
      i || (k(s), i = !0);
    },
    o(o) {
      v(s), i = !1;
    },
    d(o) {
      o && X(t), s && s.d(o);
    }
  };
}
function he(e, t, i) {
  let s, o, n;
  const r = M(() => import("./progress-5N_qOJb2.js"));
  let {
    gradio: c
  } = t, {
    props: l = {}
  } = t;
  const _ = g(l);
  x(e, _, (a) => i(15, s = a));
  let {
    _internal: d = {}
  } = t, {
    percent: f = 0
  } = t, {
    as_item: p
  } = t, {
    visible: u = !0
  } = t, {
    elem_id: h = ""
  } = t, {
    elem_classes: C = []
  } = t, {
    elem_style: K = {}
  } = t;
  const [N, F] = J({
    gradio: c,
    props: s,
    _internal: d,
    percent: f,
    visible: u,
    elem_id: h,
    elem_classes: C,
    elem_style: K,
    as_item: p
  });
  x(e, N, (a) => i(0, o = a));
  const z = G();
  return x(e, z, (a) => i(1, n = a)), e.$$set = (a) => {
    "gradio" in a && i(6, c = a.gradio), "props" in a && i(7, l = a.props), "_internal" in a && i(8, d = a._internal), "percent" in a && i(9, f = a.percent), "as_item" in a && i(10, p = a.as_item), "visible" in a && i(11, u = a.visible), "elem_id" in a && i(12, h = a.elem_id), "elem_classes" in a && i(13, C = a.elem_classes), "elem_style" in a && i(14, K = a.elem_style);
  }, e.$$.update = () => {
    e.$$.dirty & /*props*/
    128 && _.update((a) => ({
      ...a,
      ...l
    })), e.$$.dirty & /*gradio, $updatedProps, _internal, percent, visible, elem_id, elem_classes, elem_style, as_item*/
    65344 && F({
      gradio: c,
      props: s,
      _internal: d,
      percent: f,
      visible: u,
      elem_id: h,
      elem_classes: C,
      elem_style: K,
      as_item: p
    });
  }, [o, n, r, _, N, z, c, l, d, f, p, u, h, C, K, s];
}
class ye extends te {
  constructor(t) {
    super(), ue(this, t, he, be, _e, {
      gradio: 6,
      props: 7,
      _internal: 8,
      percent: 9,
      as_item: 10,
      visible: 11,
      elem_id: 12,
      elem_classes: 13,
      elem_style: 14
    });
  }
  get gradio() {
    return this.$$.ctx[6];
  }
  set gradio(t) {
    this.$$set({
      gradio: t
    }), b();
  }
  get props() {
    return this.$$.ctx[7];
  }
  set props(t) {
    this.$$set({
      props: t
    }), b();
  }
  get _internal() {
    return this.$$.ctx[8];
  }
  set _internal(t) {
    this.$$set({
      _internal: t
    }), b();
  }
  get percent() {
    return this.$$.ctx[9];
  }
  set percent(t) {
    this.$$set({
      percent: t
    }), b();
  }
  get as_item() {
    return this.$$.ctx[10];
  }
  set as_item(t) {
    this.$$set({
      as_item: t
    }), b();
  }
  get visible() {
    return this.$$.ctx[11];
  }
  set visible(t) {
    this.$$set({
      visible: t
    }), b();
  }
  get elem_id() {
    return this.$$.ctx[12];
  }
  set elem_id(t) {
    this.$$set({
      elem_id: t
    }), b();
  }
  get elem_classes() {
    return this.$$.ctx[13];
  }
  set elem_classes(t) {
    this.$$set({
      elem_classes: t
    }), b();
  }
  get elem_style() {
    return this.$$.ctx[14];
  }
  set elem_style(t) {
    this.$$set({
      elem_style: t
    }), b();
  }
}
export {
  ye as I,
  ge as g,
  g as w
};
